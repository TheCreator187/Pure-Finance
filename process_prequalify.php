<?php
/**
 * Pure Capital — Prequalification Submission Handler
 * Saves leads to submissions/prequalification/ for CRM on aminaspeace.com.
 */

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed.']);
    exit;
}

$submissionsDir = __DIR__ . '/submissions';
$prequalDir = $submissionsDir . '/prequalification';
$leadsDir = $prequalDir . '/leads';

foreach ([$submissionsDir, $prequalDir, $leadsDir] as $dir) {
    if (!is_dir($dir) && !mkdir($dir, 0750, true)) {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => 'Unable to create storage directory.']);
        exit;
    }
}

$indexFeed = $prequalDir . '/index.jsonl';

function sanitize(string $value): string {
    return htmlspecialchars(strip_tags(trim($value)), ENT_QUOTES, 'UTF-8');
}

function sanitizeEmail(string $value): string {
    $email = filter_var(trim($value), FILTER_SANITIZE_EMAIL);
    return filter_var($email, FILTER_VALIDATE_EMAIL) ? $email : '';
}

$required = [
    'business_legal_name', 'industry', 'legal_entity', 'business_start_date', 'ein',
    'company_street', 'company_city', 'company_state', 'company_zip', 'contact_method',
    'business_email', 'business_phone',
    'owner_first_name', 'owner_last_name', 'ownership_pct', 'owner_dob', 'owner_ssn',
    'owner_street', 'owner_city', 'owner_state', 'owner_zip', 'owner_email', 'owner_mobile', 'owner_fico',
];

foreach ($required as $field) {
    if (empty(trim($_POST[$field] ?? ''))) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Please fill in all required fields.']);
        exit;
    }
}

if (empty($_POST['terms_accepted'])) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Please accept the terms and authorization.']);
    exit;
}

$businessEmail = sanitizeEmail($_POST['business_email'] ?? '');
$ownerEmail = sanitizeEmail($_POST['owner_email'] ?? '');
if ($businessEmail === '' || $ownerEmail === '') {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Please enter valid email addresses.']);
    exit;
}

$ownerSsnDigits = preg_replace('/\D/', '', $_POST['owner_ssn'] ?? '');
if (strlen($ownerSsnDigits) !== 9) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Please enter a valid owner Social Security Number.']);
    exit;
}

if (!empty($_POST['co_owner_ssn'])) {
    $coSsnDigits = preg_replace('/\D/', '', $_POST['co_owner_ssn']);
    if (strlen($coSsnDigits) !== 9) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Please enter a valid co-owner Social Security Number.']);
        exit;
    }
}

$ownerSigData = trim($_POST['owner_signature_data'] ?? '');
$ownerSigName = trim($_POST['owner_signature_name'] ?? '');
if ($ownerSigData === '' && $ownerSigName === '') {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Owner signature or typed name is required.']);
    exit;
}

$requiredFiles = ['bank_statement_1', 'bank_statement_2', 'voided_check', 'owner_id'];
foreach ($requiredFiles as $fileField) {
    if (empty($_FILES[$fileField]['name']) || $_FILES[$fileField]['error'] !== UPLOAD_ERR_OK) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Please upload all required documents.']);
        exit;
    }
}

$maxSize = 10 * 1024 * 1024;
$allowedExt = ['pdf', 'jpg', 'jpeg', 'png'];

function saveSignature(string $dataUrl, string $destPath): bool {
    if ($dataUrl === '' || !str_starts_with($dataUrl, 'data:image/png;base64,')) {
        return false;
    }
    $raw = base64_decode(substr($dataUrl, strlen('data:image/png;base64,')));
    return $raw !== false && file_put_contents($destPath, $raw, LOCK_EX) !== false;
}

$id = date('Y-m-d_H-i-s') . '_' . bin2hex(random_bytes(4));
$leadDir = $leadsDir . '/' . $id;
$submissionUploadDir = $leadDir . '/files';
if (!is_dir($leadDir) && !mkdir($leadDir, 0750, true)) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Unable to create lead directory.']);
    exit;
}
if (!mkdir($submissionUploadDir, 0750, true)) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Unable to save uploads.']);
    exit;
}

$uploadedFiles = [];
$fileFields = [
    'bank_statement_1', 'bank_statement_2', 'bank_statement_3', 'bank_statement_4',
    'voided_check', 'owner_id', 'co_owner_id',
];

foreach ($fileFields as $fileField) {
    if (empty($_FILES[$fileField]['name']) || $_FILES[$fileField]['error'] === UPLOAD_ERR_NO_FILE) {
        continue;
    }
    if ($_FILES[$fileField]['error'] !== UPLOAD_ERR_OK) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'File upload failed. Please try again.']);
        exit;
    }
    if ($_FILES[$fileField]['size'] > $maxSize) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'One or more files exceed the 10 MB limit.']);
        exit;
    }
    $ext = strtolower(pathinfo($_FILES[$fileField]['name'], PATHINFO_EXTENSION));
    if (!in_array($ext, $allowedExt, true)) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Invalid file type. Use PDF, JPG, or PNG.']);
        exit;
    }
    $safeName = preg_replace('/[^a-z0-9._-]+/i', '_', pathinfo($_FILES[$fileField]['name'], PATHINFO_FILENAME));
    $filename = $fileField . '_' . $safeName . '.' . $ext;
    $dest = $submissionUploadDir . '/' . $filename;
    if (!move_uploaded_file($_FILES[$fileField]['tmp_name'], $dest)) {
        http_response_code(500);
        echo json_encode(['success' => false, 'message' => 'Unable to save uploaded file.']);
        exit;
    }
    $uploadedFiles[$fileField] = 'files/' . $filename;
}

$signatures = [];
if ($ownerSigData !== '') {
    $sigPath = $submissionUploadDir . '/owner_signature.png';
    if (saveSignature($ownerSigData, $sigPath)) {
        $signatures['owner'] = 'files/owner_signature.png';
    }
}
if ($ownerSigName !== '') {
    $signatures['owner_typed_name'] = sanitize($ownerSigName);
}

$coSigData = trim($_POST['co_owner_signature_data'] ?? '');
$coSigName = trim($_POST['co_owner_signature_name'] ?? '');
if ($coSigData !== '') {
    $sigPath = $submissionUploadDir . '/co_owner_signature.png';
    if (saveSignature($coSigData, $sigPath)) {
        $signatures['co_owner'] = 'files/co_owner_signature.png';
    }
}
if ($coSigName !== '') {
    $signatures['co_owner_typed_name'] = sanitize($coSigName);
}

$textFields = [
    'source_page', 'business_legal_name', 'dba', 'industry', 'industry_other', 'legal_entity', 'legal_entity_other',
    'business_start_date', 'ein', 'website', 'company_street', 'company_city', 'company_state', 'company_zip',
    'contact_method', 'business_email', 'business_phone',
    'owner_first_name', 'owner_last_name', 'ownership_pct', 'owner_dob', 'owner_street', 'owner_city',
    'owner_state', 'owner_zip', 'owner_email', 'owner_mobile', 'owner_fico',
    'co_owner_first_name', 'co_owner_last_name', 'co_ownership_pct', 'co_owner_dob', 'co_owner_street',
    'co_owner_city', 'co_owner_state', 'co_owner_zip', 'co_owner_email', 'co_owner_mobile', 'co_owner_fico',
    'owner_signature_name', 'co_owner_signature_name',
];

$data = ['submission_id' => $id, 'type' => 'prequalification'];
foreach ($textFields as $field) {
    if (isset($_POST[$field]) && $_POST[$field] !== '') {
        if (in_array($field, ['business_email', 'owner_email', 'co_owner_email'], true)) {
            $data[$field] = sanitizeEmail((string) $_POST[$field]);
        } elseif (in_array($field, ['owner_ssn', 'co_owner_ssn'], true)) {
            continue;
        } else {
            $data[$field] = sanitize((string) $_POST[$field]);
        }
    }
}

$data['owner_ssn_last4'] = substr($ownerSsnDigits, -4);
if (!empty($_POST['co_owner_ssn'])) {
    $data['co_owner_ssn_last4'] = substr(preg_replace('/\D/', '', $_POST['co_owner_ssn']), -4);
}

$mca = [];
for ($i = 1; $i <= 5; $i++) {
    $row = [
        'lender' => sanitize((string) ($_POST["mca_lender_$i"] ?? '')),
        'original' => sanitize((string) ($_POST["mca_original_$i"] ?? '')),
        'balance' => sanitize((string) ($_POST["mca_balance_$i"] ?? '')),
        'payment' => sanitize((string) ($_POST["mca_payment_$i"] ?? '')),
        'status' => sanitize((string) ($_POST["mca_status_$i"] ?? '')),
    ];
    if (implode('', $row) !== '') {
        $mca[] = $row;
    }
}
if ($mca) {
    $data['mca_positions'] = $mca;
}

$re = [];
for ($i = 1; $i <= 3; $i++) {
    $row = [
        'address' => sanitize((string) ($_POST["re_address_$i"] ?? '')),
        'type' => sanitize((string) ($_POST["re_type_$i"] ?? '')),
        'value' => sanitize((string) ($_POST["re_value_$i"] ?? '')),
        'mortgage' => sanitize((string) ($_POST["re_mortgage_$i"] ?? '')),
        'payment' => sanitize((string) ($_POST["re_payment_$i"] ?? '')),
    ];
    if (implode('', $row) !== '') {
        $re[] = $row;
    }
}
if ($re) {
    $data['real_estate'] = $re;
}

$data['uploads'] = $uploadedFiles;
$data['signatures'] = $signatures;
$data['terms_accepted'] = true;
$data['submitted_at'] = date('Y-m-d H:i:s T');
$data['ip_address'] = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$data['user_agent'] = sanitize($_SERVER['HTTP_USER_AGENT'] ?? 'unknown');
$data['referrer'] = sanitize($_SERVER['HTTP_REFERER'] ?? '');

$data['lead_dir'] = $leadDir;
$data['crm_inbox'] = 'submissions/prequalification';

$leadJsonPath = $leadDir . '/lead.json';
$json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
if (file_put_contents($leadJsonPath, $json, LOCK_EX) === false) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Unable to save your prequalification. Please call us directly.']);
    exit;
}

$ownerName = trim(($data['owner_first_name'] ?? '') . ' ' . ($data['owner_last_name'] ?? ''));
$crm = [
    'submission_id' => $id,
    'type' => 'prequalification',
    'source' => 'purecapital.us',
    'crm_host' => 'aminaspeace.com',
    'submitted_at' => $data['submitted_at'],
    'lead_dir' => $leadDir,
    'lead_json' => $leadJsonPath,
    'server_path' => $leadDir,
    'business_legal_name' => $data['business_legal_name'] ?? '',
    'dba' => $data['dba'] ?? '',
    'industry' => $data['industry'] ?? '',
    'legal_entity' => $data['legal_entity'] ?? '',
    'ein' => $data['ein'] ?? '',
    'business_email' => $businessEmail,
    'business_phone' => $data['business_phone'] ?? '',
    'contact_method' => $data['contact_method'] ?? '',
    'owner_name' => $ownerName,
    'owner_email' => $ownerEmail,
    'owner_mobile' => $data['owner_mobile'] ?? '',
    'owner_fico' => $data['owner_fico'] ?? '',
    'ownership_pct' => $data['ownership_pct'] ?? '',
    'owner_ssn_last4' => $data['owner_ssn_last4'] ?? '',
    'file_count' => count($uploadedFiles),
    'files' => array_map(
        static fn (string $rel): array => ['relative' => $rel, 'absolute' => $leadDir . '/' . $rel],
        array_values($uploadedFiles)
    ),
    'signatures' => $signatures,
];
file_put_contents($leadDir . '/crm.json', json_encode($crm, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);

$feedLine = json_encode([
    'submission_id' => $id,
    'submitted_at' => $data['submitted_at'],
    'lead_dir' => $leadDir,
    'business_legal_name' => $crm['business_legal_name'],
    'owner_name' => $ownerName,
    'owner_email' => $ownerEmail,
    'owner_mobile' => $crm['owner_mobile'],
    'owner_fico' => $crm['owner_fico'],
    'industry' => $crm['industry'],
    'processed' => false,
], JSON_UNESCAPED_UNICODE) . PHP_EOL;
file_put_contents($indexFeed, $feedLine, FILE_APPEND | LOCK_EX);

$logLine = date('Y-m-d H:i:s') . ' | ' . $ownerName
    . ' | ' . $data['business_legal_name'] . ' | ' . ($data['owner_fico'] ?? '')
    . ' | ' . count($uploadedFiles) . ' files | ' . $id . PHP_EOL;
file_put_contents($prequalDir . '/_ingest.log', $logLine, FILE_APPEND | LOCK_EX);

echo json_encode(['success' => true, 'message' => 'Prequalification received successfully.', 'id' => $id]);
