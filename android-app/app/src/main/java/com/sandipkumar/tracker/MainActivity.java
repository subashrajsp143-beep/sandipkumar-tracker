package com.sandipkumar.tracker;

import android.Manifest;
import android.app.DownloadManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.provider.MediaStore;
import android.view.View;
import android.webkit.CookieManager;
import android.webkit.DownloadListener;
import android.webkit.GeolocationPermissions;
import android.webkit.URLUtil;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.OnBackPressedCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {

    private static final String APP_URL = "https://sandipkumar-tracker.onrender.com";
    private static final int MAX_AUTO_RETRIES = 5;

    private WebView webView;
    private ProgressBar progressBar;
    private View errorLayout;
    private Button btnRetry;
    private TextView errorTitle;
    private TextView errorSubtitle;
    private TextView autoRetryCountdown;
    private ProgressBar retrySpinner;

    private ValueCallback<Uri[]> uploadMessage;
    private Uri cameraImageUri;

    private String pendingGeoOrigin;
    private GeolocationPermissions.Callback pendingGeoCallback;

    private ActivityResultLauncher<Intent> fileChooserLauncher;
    private ActivityResultLauncher<String[]> permissionLauncher;

    private int retryCount = 0;
    private CountDownTimer retryTimer;
    private final Handler mainHandler = new Handler(Looper.getMainLooper());

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webView);
        progressBar = findViewById(R.id.progressBar);
        errorLayout = findViewById(R.id.errorLayout);
        btnRetry = findViewById(R.id.btnRetry);
        errorTitle = findViewById(R.id.errorTitle);
        errorSubtitle = findViewById(R.id.errorSubtitle);
        autoRetryCountdown = findViewById(R.id.autoRetryCountdown);
        retrySpinner = findViewById(R.id.retrySpinner);

        setupLaunchers();
        requestRequiredPermissions();
        configureWebView();

        btnRetry.setOnClickListener(v -> {
            cancelRetryTimer();
            retryCount = 0;
            showLoadingState();
            webView.loadUrl(APP_URL);
        });

        // Handle hardware back button navigation
        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                if (errorLayout.getVisibility() == View.VISIBLE) {
                    finish();
                } else if (webView.canGoBack()) {
                    webView.goBack();
                } else {
                    finish();
                }
            }
        });

        if (savedInstanceState != null) {
            webView.restoreState(savedInstanceState);
        } else {
            showLoadingState();
            webView.loadUrl(APP_URL);
        }
    }

    private void setupLaunchers() {
        // File chooser launcher (Camera & Gallery upload)
        fileChooserLauncher = registerForActivityResult(
                new ActivityResultContracts.StartActivityForResult(),
                result -> {
                    if (uploadMessage == null) return;
                    Uri[] results = null;
                    if (result.getResultCode() == RESULT_OK) {
                        Intent data = result.getData();
                        if (data != null && data.getData() != null) {
                            results = new Uri[]{data.getData()};
                        } else if (cameraImageUri != null) {
                            results = new Uri[]{cameraImageUri};
                        }
                    }
                    uploadMessage.onReceiveValue(results);
                    uploadMessage = null;
                }
        );

        // Runtime permissions launcher (Location, Camera, Storage)
        permissionLauncher = registerForActivityResult(
                new ActivityResultContracts.RequestMultiplePermissions(),
                result -> {
                    Boolean fineGranted = result.get(Manifest.permission.ACCESS_FINE_LOCATION);
                    Boolean coarseGranted = result.get(Manifest.permission.ACCESS_COARSE_LOCATION);
                    boolean locationOk = (fineGranted != null && fineGranted) || (coarseGranted != null && coarseGranted);

                    if (locationOk && pendingGeoCallback != null && pendingGeoOrigin != null) {
                        pendingGeoCallback.invoke(pendingGeoOrigin, true, false);
                        pendingGeoCallback = null;
                        pendingGeoOrigin = null;
                    }
                }
        );
    }

    private void requestRequiredPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            permissionLauncher.launch(new String[]{
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION,
                    Manifest.permission.CAMERA,
                    Manifest.permission.READ_MEDIA_IMAGES
            });
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            permissionLauncher.launch(new String[]{
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION,
                    Manifest.permission.CAMERA,
                    Manifest.permission.READ_EXTERNAL_STORAGE
            });
        } else {
            permissionLauncher.launch(new String[]{
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION,
                    Manifest.permission.CAMERA,
                    Manifest.permission.READ_EXTERNAL_STORAGE,
                    Manifest.permission.WRITE_EXTERNAL_STORAGE
            });
        }
    }

    private void configureWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setGeolocationEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);

        // 1:1 Pixel-Perfect Mobile Viewport Calibration:
        // setUseWideViewPort(true) enables WebView to honor the HTML viewport meta tag
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setTextZoom(100); // Prevents Android OS Accessibility font blowout
        settings.setSupportZoom(false); // Disables accidental pinch-to-zoom stretching
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setLayoutAlgorithm(WebSettings.LayoutAlgorithm.NORMAL);
        settings.setDefaultTextEncodingName("utf-8");
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);
        settings.setMediaPlaybackRequiresUserGesture(false);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }

        // Hardware accelerated smooth native scrolling
        webView.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
        webView.setOverScrollMode(View.OVER_SCROLL_IF_CONTENT_SCROLLS);
        webView.setVerticalScrollBarEnabled(true);
        webView.setHorizontalScrollBarEnabled(false);
        webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);

        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(webView, true);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                return handleSpecialUrls(url);
            }

            @SuppressWarnings("deprecation")
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return handleSpecialUrls(url);
            }

            @Override
            public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                progressBar.setVisibility(View.VISIBLE);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                progressBar.setVisibility(View.GONE);
                cancelRetryTimer();
                retryCount = 0;
                errorLayout.setVisibility(View.GONE);
                webView.setVisibility(View.VISIBLE);
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request.isForMainFrame()) {
                    handlePageError();
                }
            }

            @SuppressWarnings("deprecation")
            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                handlePageError();
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                if (newProgress < 100) {
                    progressBar.setVisibility(View.VISIBLE);
                    progressBar.setProgress(newProgress);
                } else {
                    progressBar.setVisibility(View.GONE);
                }
            }

            // Auto-grant Geolocation to the site
            @Override
            public void onGeolocationPermissionsShowPrompt(String origin, GeolocationPermissions.Callback callback) {
                boolean hasFine = ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED;
                boolean hasCoarse = ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED;

                if (hasFine || hasCoarse) {
                    callback.invoke(origin, true, false);
                } else {
                    pendingGeoOrigin = origin;
                    pendingGeoCallback = callback;
                    permissionLauncher.launch(new String[]{
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION
                    });
                }
            }

            // File Chooser for Camera Capture & Photo Attendance Uploads
            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
                if (uploadMessage != null) {
                    uploadMessage.onReceiveValue(null);
                }
                uploadMessage = filePathCallback;

                Intent takePictureIntent = null;
                try {
                    File photoFile = createImageFile();
                    if (photoFile != null) {
                        String authority = getPackageName() + ".fileprovider";
                        cameraImageUri = FileProvider.getUriForFile(MainActivity.this, authority, photoFile);
                        takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                        takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, cameraImageUri);
                        takePictureIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
                    }
                } catch (Throwable t) {
                    cameraImageUri = null;
                }

                Intent contentSelectionIntent = new Intent(Intent.ACTION_GET_CONTENT);
                contentSelectionIntent.addCategory(Intent.CATEGORY_OPENABLE);
                contentSelectionIntent.setType("image/*");

                Intent chooserIntent = new Intent(Intent.ACTION_CHOOSER);
                chooserIntent.putExtra(Intent.EXTRA_INTENT, contentSelectionIntent);
                chooserIntent.putExtra(Intent.EXTRA_TITLE, "फोटो चुनें या कैमरा से खींचें");

                if (takePictureIntent != null) {
                    chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, new Intent[]{takePictureIntent});
                }

                try {
                    fileChooserLauncher.launch(chooserIntent);
                    return true;
                } catch (Throwable t) {
                    if (uploadMessage != null) {
                        uploadMessage.onReceiveValue(null);
                        uploadMessage = null;
                    }
                    return false;
                }
            }
        });

        // Download handling for Excel and PDF reports
        webView.setDownloadListener(new DownloadListener() {
            @Override
            public void onDownloadStart(String url, String userAgent, String contentDisposition, String mimeType, long contentLength) {
                try {
                    DownloadManager.Request request = new DownloadManager.Request(Uri.parse(url));
                    request.setMimeType(mimeType);
                    String cookies = CookieManager.getInstance().getCookie(url);
                    request.addRequestHeader("cookie", cookies);
                    request.addRequestHeader("User-Agent", userAgent);
                    request.setDescription("डाउनलोड हो रहा है...");
                    String filename = URLUtil.guessFileName(url, contentDisposition, mimeType);
                    request.setTitle(filename);
                    request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
                    request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, filename);

                    DownloadManager dm = (DownloadManager) getSystemService(Context.DOWNLOAD_SERVICE);
                    if (dm != null) {
                        dm.enqueue(request);
                        Toast.makeText(MainActivity.this, "फाइल डाउनलोड हो रही है: " + filename, Toast.LENGTH_SHORT).show();
                    }
                } catch (Exception e) {
                    try {
                        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                        startActivity(intent);
                    } catch (Exception ignored) {}
                }
            }
        });
    }

    private boolean handleSpecialUrls(String url) {
        if (url == null) return false;

        // Open external dialer, WhatsApp, email, maps in native apps
        if (url.startsWith("tel:") || url.startsWith("mailto:") ||
                url.startsWith("whatsapp:") || url.startsWith("geo:") ||
                url.contains("maps.google.com") || url.contains("api.whatsapp.com")) {
            try {
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                startActivity(intent);
                return true;
            } catch (Exception ignored) {
                return false;
            }
        }

        // Keep app navigation inside WebView
        return false;
    }

    private File createImageFile() {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(new Date());
        String imageFileName = "IMG_" + timeStamp + "_";

        // Primary: App external pictures dir
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        if (storageDir != null && (storageDir.exists() || storageDir.mkdirs())) {
            try {
                return File.createTempFile(imageFileName, ".jpg", storageDir);
            } catch (IOException ignored) {}
        }

        // Secondary: Cache dir
        File cacheDir = getCacheDir();
        if (cacheDir != null && (cacheDir.exists() || cacheDir.mkdirs())) {
            try {
                return File.createTempFile(imageFileName, ".jpg", cacheDir);
            } catch (IOException ignored) {}
        }

        // Fallback: Internal files dir
        return new File(getFilesDir(), imageFileName + ".jpg");
    }

    private void showLoadingState() {
        progressBar.setVisibility(View.VISIBLE);
        errorLayout.setVisibility(View.GONE);
        webView.setVisibility(View.VISIBLE);
    }

    private void handlePageError() {
        progressBar.setVisibility(View.GONE);
        webView.setVisibility(View.GONE);
        errorLayout.setVisibility(View.VISIBLE);

        if (retryCount < MAX_AUTO_RETRIES) {
            retryCount++;
            startAutoRetryCountdown(6);
        } else {
            retrySpinner.setVisibility(View.GONE);
            autoRetryCountdown.setText("कृपया अपना इंटरनेट जांचें और 'दोबारा प्रयास करें' बटन दबाएं।");
        }
    }

    private void startAutoRetryCountdown(int seconds) {
        cancelRetryTimer();
        retrySpinner.setVisibility(View.VISIBLE);

        retryTimer = new CountDownTimer(seconds * 1000L, 1000L) {
            @Override
            public void onTick(long millisUntilFinished) {
                long sec = (millisUntilFinished / 1000L) + 1;
                autoRetryCountdown.setText("सर्वर चालू (Wake Up) हो रहा है... " + sec + " सेकंड में पुनः प्रयास (" + retryCount + "/" + MAX_AUTO_RETRIES + ")");
            }

            @Override
            public void onFinish() {
                autoRetryCountdown.setText("कनेक्ट किया जा रहा है...");
                webView.loadUrl(APP_URL);
            }
        }.start();
    }

    private void cancelRetryTimer() {
        if (retryTimer != null) {
            retryTimer.cancel();
            retryTimer = null;
        }
    }

    @Override
    protected void onDestroy() {
        cancelRetryTimer();
        if (webView != null) {
            webView.destroy();
        }
        super.onDestroy();
    }

    @Override
    protected void onSaveInstanceState(@NonNull Bundle outState) {
        super.onSaveInstanceState(outState);
        webView.saveState(outState);
    }
}
