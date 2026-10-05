import 'dart:convert';

class StudyTask {
  final String id, title, subject;
  final DateTime deadline;
  final int minutes;
  final bool done;
  const StudyTask({
    required this.id,
    required this.title,
    required this.subject,
    required this.deadline,
    required this.minutes,
    this.done = false,
  });
  StudyTask toggle() => StudyTask(
    id: id,
    title: title,
    subject: subject,
    deadline: deadline,
    minutes: minutes,
    done: !done,
  );
  Map<String, Object> toJson() => {
    'id': id,
    'title': title,
    'subject': subject,
    'deadline': dateString(deadline),
    'minutes': minutes,
    'done': done,
  };
  static StudyTask fromJson(Object? value) {
    if (value is! Map<String, dynamic>)
      throw const FormatException('Tarefa inválida.');
    for (final key in ['id', 'title', 'subject']) {
      if (value[key] is! String ||
          (value[key] as String).trim().isEmpty ||
          (value[key] as String).length > 200)
        throw FormatException('Campo $key inválido.');
    }
    final raw = value['deadline'];
    if (raw is! String || !RegExp(r'^\d{4}-\d{2}-\d{2}$').hasMatch(raw))
      throw const FormatException('Data inválida.');
    final date = DateTime.tryParse(raw);
    if (date == null ||
        dateString(date) != raw ||
        date.year < 1900 ||
        date.year > 2200)
      throw const FormatException('Data inválida.');
    if (value['minutes'] is! int ||
        value['minutes'] < 1 ||
        value['minutes'] > 1440 ||
        value['done'] is! bool)
      throw const FormatException('Duração ou conclusão inválida.');
    return StudyTask(
      id: value['id'],
      title: value['title'],
      subject: value['subject'],
      deadline: date,
      minutes: value['minutes'],
      done: value['done'],
    );
  }
}

String dateString(DateTime d) =>
    '${d.year.toString().padLeft(4, '0')}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';
String encodeBackup(List<StudyTask> tasks) => const JsonEncoder.withIndent('  ')
    .convert({'version': 1, 'tasks': tasks.map((t) => t.toJson()).toList()});
List<StudyTask> decodeBackup(String text) {
  if (text.length > 2000000)
    throw const FormatException('Backup excede 2 MB de texto.');
  final data = jsonDecode(text);
  if (data is! Map<String, dynamic> ||
      data['version'] is! int ||
      data['version'] != 1 ||
      data['tasks'] is! List)
    throw const FormatException('Formato ou versão de backup incompatível.');
  final rows = data['tasks'] as List;
  if (rows.length > 5000)
    throw const FormatException('Limite de 5.000 tarefas.');
  final tasks = rows.map(StudyTask.fromJson).toList();
  if (tasks.map((t) => t.id).toSet().length != tasks.length)
    throw const FormatException('Backup contém identificadores duplicados.');
  return tasks;
}
