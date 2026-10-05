// Browser-only persistence; no network requests.
// Kept in this isolated conditional implementation to avoid external dependencies.
// Migration to dart:js_interop is required before enabling a Wasm build.
// ignore: deprecated_member_use
import 'dart:html' as html;

String? loadData() => html.window.localStorage['estudaoffline.v1'];
void saveData(String text) {
  html.window.localStorage['estudaoffline.v1'] = text;
}

void downloadBackup(String text) {
  final blob = html.Blob([text], 'application/json');
  final url = html.Url.createObjectUrlFromBlob(blob);
  final link = html.AnchorElement(href: url)
    ..download = 'estudaoffline-backup.json';
  html.document.body!.append(link);
  link.click();
  link.remove();
  html.Url.revokeObjectUrl(url);
}
