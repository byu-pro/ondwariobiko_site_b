<?php

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method Not Allowed');
}

// Honeypot bot protection (if honeypot field is filled out, reject request)
if (!empty($_POST['website_hp'])) {
    http_response_code(200);
    exit('Success');
}

// Hardcoded recipient email address to prevent Open Mail Relay vulnerabilities
$admin_email = 'ondwariobiko@gmail.com';

// Sanitize project name and form subject
$project_name_raw = isset($_POST['project_name']) ? $_POST['project_name'] : 'Ondwari Obiko Portfolio';
$form_subject_raw = isset($_POST['form_subject']) ? $_POST['form_subject'] : 'New Contact Inquiry';

// Prevent header injection by removing newlines
$project_name = preg_replace('/[\r\n]+/', ' ', trim($project_name_raw));
$form_subject = preg_replace('/[\r\n]+/', ' ', trim($form_subject_raw));

// Extract and sanitize sender reply-to email if provided
$user_email = '';
if (!empty($_POST['email'])) {
    $clean_user_email = filter_var(trim($_POST['email']), FILTER_VALIDATE_EMAIL);
    if ($clean_user_email) {
        $user_email = $clean_user_email;
    }
}
if (empty($user_email)) {
    $user_email = $admin_email;
}

// Construct sanitized HTML message body
$c = true;
$message_rows = '';

foreach ($_POST as $key => $value) {
    if (!empty($value) && !in_array($key, ['project_name', 'admin_email', 'form_subject', 'website_hp'])) {
        $safe_key   = htmlspecialchars(trim($key), ENT_QUOTES, 'UTF-8');
        $safe_value = nl2br(htmlspecialchars(trim($value), ENT_QUOTES, 'UTF-8'));
        
        $bg_style = ($c = !$c) ? 'background-color: #ffffff;' : 'background-color: #f8f8f8;';
        $message_rows .= "<tr style='{$bg_style}'>
            <td style='padding: 10px; border: 1px solid #e9e9e9; font-weight: bold; width: 30%;'>{$safe_key}</td>
            <td style='padding: 10px; border: 1px solid #e9e9e9;'>{$safe_value}</td>
        </tr>";
    }
}

$message = "<table style='width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; color: #333;'>{$message_rows}</table>";

function adopt($text) {
    return '=?UTF-8?B?' . base64_encode($text) . '?=';
}

// Set secure headers
$headers  = "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/html; charset=utf-8\r\n";
$headers .= "From: " . adopt($project_name) . " <no-reply@" . ($_SERVER['SERVER_NAME'] ?? 'ondwariobiko.com') . ">\r\n";
$headers .= "Reply-To: " . $user_email . "\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

// Send mail safely
$success = @mail($admin_email, adopt($form_subject), $message, $headers);

if ($success) {
    echo "OK";
} else {
    http_response_code(500);
    echo "Error sending email";
}
?>
