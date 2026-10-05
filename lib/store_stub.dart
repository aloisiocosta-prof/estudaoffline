String? _data;
String? loadData() => _data;
void saveData(String text) {
  _data = text;
}

void downloadBackup(String text) {
  throw UnsupportedError('Download disponível na versão web.');
}
