<?php
/**
 * Pure Capital — Application Submission Handler
 * Saves each application to submissions/ as an individual JSON file.
 */

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed.']);
    exit;
}

$submissionsDir = __DIR__ . '/submissions';

if (!is_dir($submissionsDir)) {
    if (!mkdir($submissionsDir, 0750, true)) {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => 'Unable to create submissions directory.']);
        exit;
    }
}

$required = ['first_name', 'last_name', 'email', 'phone', 'business_name', 'funding_amount'];

foreach ($required as $field) {
    if (empty(trim($_POST[$field] ?? ''))) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Please fill in all required fields.']);
        exit;
    }
}

function sanitize(string $value): string {
    return htmlspecialchars(strip_tags(trim($value)), ENT_QUOTES, 'UTF-8');
}

function sanitizeEmail(string $value): string {
    $email = filter_var(trim($value), FILTER_SANITIZE_EMAIL);
    return filter_var($email, FILTER_VALIDATE_EMAIL) ? $email : '';
}

$email = sanitizeEmail($_POST['email'] ?? '');
if ($email === '') {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Please enter a valid email address.']);
    exit;
}

$sourcePage = trim($_POST['source_page'] ?? '');
if ($sourcePage === 'apply.html' && empty(trim($_POST['ssn'] ?? ''))) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Please enter your Social Security Number.']);
    exit;
}

if (!empty($_POST['ssn'])) {
    $ssnDigits = preg_replace('/\D/', '', $_POST['ssn']);
    if (strlen($ssnDigits) !== 9) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Please enter a valid 9-digit Social Security Number.']);
        exit;
    }
}

$allowedFields = [
    'first_name', 'last_name', 'email', 'phone', 'ssn', 'business_name',
    'business_type', 'years_in_business', 'monthly_revenue', 'funding_amount',
    'loan_type', 'funds_purpose', 'state', 'city', 'zip', 'ein',
    'source_page', 'message'
];

$data = [];
foreach ($allowedFields as $field) {
    if (isset($_POST[$field]) && $_POST[$field] !== '') {
        if ($field === 'email') {
            $data[$field] = $email;
        } elseif ($field === 'ssn') {
            $data[$field] = substr(preg_replace('/\D/', '', $_POST['ssn']), 0, 9);
        } else {
            $data[$field] = sanitize((string) $_POST[$field]);
        }
    }
}

$data['submitted_at'] = date('Y-m-d H:i:s T');
$data['ip_address'] = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$data['user_agent'] = sanitize($_SERVER['HTTP_USER_AGENT'] ?? 'unknown');
$data['referrer'] = sanitize($_SERVER['HTTP_REFERER'] ?? '');

$id = date('Y-m-d_H-i-s') . '_' . bin2hex(random_bytes(4));
$businessSlug = preg_replace('/[^a-z0-9]+/i', '-', strtolower($data['business_name']));
$businessSlug = trim(substr($businessSlug, 0, 40), '-');
$filename = $id . ($businessSlug ? '_' . $businessSlug : '') . '.json';
$filepath = $submissionsDir . '/' . $filename;

$json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);

if (file_put_contents($filepath, $json, LOCK_EX) === false) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Unable to save your application. Please call us directly.']);
    exit;
}

// Append to master log for easy browsing
$logLine = date('Y-m-d H:i:s') . ' | ' . $data['first_name'] . ' ' . $data['last_name']
    . ' | ' . $data['business_name'] . ' | ' . ($data['funding_amount'] ?? 'N/A')
    . ' | ' . ($data['loan_type'] ?? 'General') . ' | ' . $filename . PHP_EOL;
file_put_contents($submissionsDir . '/_applications.log', $logLine, FILE_APPEND | LOCK_EX);

$acceptsJson = isset($_SERVER['HTTP_ACCEPT']) && str_contains($_SERVER['HTTP_ACCEPT'], 'application/json');
$isAjax = isset($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest';

if ($isAjax || $acceptsJson) {
    echo json_encode(['success' => true, 'message' => 'Application received successfully.', 'id' => $id]);
    exit;
}

header('Location: thank-you.html');
exit;
