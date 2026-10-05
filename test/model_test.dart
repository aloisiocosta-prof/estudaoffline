import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:estudaoffline/model.dart';

void main() {
  final task = StudyTask(
    id: 'a',
    title: 'Revisar',
    subject: 'Matemática',
    deadline: DateTime(2026, 10, 10),
    minutes: 30,
  );
  test('backup preserva todos os campos e conclusão', () {
    final decoded = decodeBackup(encodeBackup([task.toggle()]));
    expect(decoded.single.toJson(), task.toggle().toJson());
    expect(task.done, false);
    expect(task.toggle().toggle().done, false);
  });
  test('rejeita JSON corrompido e versão desconhecida', () {
    for (final text in [
      '{',
      '{"version":2,"tasks":[]}',
      '{"version":"1","tasks":[]}',
      '[]',
    ]) {
      expect(() => decodeBackup(text), throwsFormatException);
    }
  });
  test('rejeita IDs duplicados', () {
    expect(
      () => decodeBackup(encodeBackup([task, task])),
      throwsFormatException,
    );
  });
  test('rejeita data normalizada silenciosamente e tipos incorretos', () {
    for (final mutation in [
      {'deadline': '2026-02-30'},
      {'minutes': 0},
      {'minutes': 30.5},
      {'done': 'false'},
      {'title': ''},
      {'subject': null},
    ]) {
      final row = {...task.toJson(), ...mutation};
      expect(
        () => decodeBackup(
          jsonEncode({
            'version': 1,
            'tasks': [row],
          }),
        ),
        throwsFormatException,
      );
    }
  });
  test('validação completa impede retorno parcial de backup', () {
    final existing = [task];
    expect(
      () => decodeBackup(
        jsonEncode({
          'version': 1,
          'tasks': [
            task.toJson(),
            {'id': 'broken'},
          ],
        }),
      ),
      throwsFormatException,
    );
    expect(existing.single.toJson(), task.toJson());
  });
}
