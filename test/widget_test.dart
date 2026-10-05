import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:estudaoffline/main.dart';
import 'package:estudaoffline/store_stub.dart' as store;

void main() {
  testWidgets('cria tarefa, conclui, filtra e mantém após reconstrução', (
    tester,
  ) async {
    store.saveData('{"version":1,"tasks":[]}');
    await tester.pumpWidget(const EstudaOffline());
    await tester.tap(find.text('Nova tarefa'));
    await tester.pumpAndSettle();
    final fields = find.byType(TextFormField);
    await tester.enterText(fields.at(0), 'Preparar resumo');
    await tester.enterText(fields.at(1), 'História');
    await tester.tap(find.text('Adicionar'));
    await tester.pumpAndSettle();
    expect(find.text('Preparar resumo'), findsWidgets);
    await tester.tap(find.text('Tarefas'));
    await tester.pumpAndSettle();
    await tester.ensureVisible(find.byType(Checkbox).first);
    await tester.tap(find.byType(Checkbox).first);
    await tester.pumpAndSettle();
    await tester.tap(find.text('Concluídas'));
    await tester.pumpAndSettle();
    expect(find.text('Preparar resumo'), findsOneWidget);
    await tester.pumpWidget(const SizedBox());
    await tester.pumpWidget(const EstudaOffline());
    await tester.tap(find.text('Tarefas'));
    await tester.pumpAndSettle();
    expect(find.text('Preparar resumo'), findsOneWidget);
    expect(tester.widget<Checkbox>(find.byType(Checkbox).first).value, true);
    await tester.pump(const Duration(seconds: 2));
  });
}
