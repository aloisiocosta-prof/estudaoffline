import 'package:flutter/material.dart';

import 'model.dart';
import 'store.dart' as store;

void main() => runApp(const EstudaOffline());
const navy = Color(0xFF173C45);
const teal = Color(0xFF157C73);

class EstudaOffline extends StatelessWidget {
  const EstudaOffline({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
    debugShowCheckedModeBanner: false,
    title: 'EstudaOffline',
    theme: ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(seedColor: teal),
      scaffoldBackgroundColor: const Color(0xFFF7F6F0),
      textTheme: const TextTheme(
        headlineLarge: TextStyle(color: navy, fontWeight: FontWeight.w800),
        headlineMedium: TextStyle(color: navy, fontWeight: FontWeight.w800),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Color(0xFFF7F6F0),
        foregroundColor: navy,
      ),
    ),
    home: const StudyHome(),
  );
}

class StudyHome extends StatefulWidget {
  const StudyHome({super.key});
  @override
  State<StudyHome> createState() => _StudyHomeState();
}

class _StudyHomeState extends State<StudyHome> {
  List<StudyTask> tasks = [];
  int tab = 0;
  String filter = 'Todas';
  String? loadError;
  @override
  void initState() {
    super.initState();
    try {
      final raw = store.loadData();
      if (raw != null) tasks = decodeBackup(raw);
    } catch (_) {
      loadError = 'Não foi possível ler os dados locais. Eles não foram sobrescritos. Exporte ou recupere um backup antes de continuar.';
    }
  }

  bool commit(List<StudyTask> next) {
    if (loadError != null) {
      notice(
        'Armazenamento com erro: recupere um backup válido na aba Segurança.',
      );
      return false;
    }
    try {
      store.saveData(encodeBackup(next));
      setState(() => tasks = next);
      return true;
    } catch (_) {
      notice(
        'Não foi possível salvar. Nenhuma alteração foi aplicada. Verifique o armazenamento do navegador.',
      );
      return false;
    }
  }

  void notice(String message) =>
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(message)));
  List<StudyTask> get pending =>
      tasks.where((t) => !t.done).toList()
        ..sort((a, b) => a.deadline.compareTo(b.deadline));
  @override
  Widget build(BuildContext context) {
    final wide = MediaQuery.sizeOf(context).width >= 850;
    final content = switch (tab) {
      0 => dashboard(),
      1 => taskPage(),
      _ => safetyPage(),
    };
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: teal,
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Icon(
                Icons.auto_stories_rounded,
                color: Colors.white,
              ),
            ),
            const SizedBox(width: 12),
            const Text(
              'EstudaOffline',
              style: TextStyle(fontWeight: FontWeight.w800),
            ),
            const Spacer(),
            if (wide)
              const Text(
                'SEU RITMO. SEU ESPAÇO.',
                style: TextStyle(fontSize: 12, letterSpacing: 1.2),
              ),
          ],
        ),
      ),
      body: Row(
        children: [
          if (wide)
            NavigationRail(
              selectedIndex: tab,
              onDestinationSelected: (v) => setState(() => tab = v),
              labelType: NavigationRailLabelType.all,
              backgroundColor: const Color(0xFFF7F6F0),
              destinations: const [
                NavigationRailDestination(
                  icon: Icon(Icons.space_dashboard_outlined),
                  label: Text('Painel'),
                ),
                NavigationRailDestination(
                  icon: Icon(Icons.checklist_rounded),
                  label: Text('Tarefas'),
                ),
                NavigationRailDestination(
                  icon: Icon(Icons.shield_outlined),
                  label: Text('Segurança'),
                ),
              ],
            ),
          Expanded(
            child: SingleChildScrollView(
              padding: EdgeInsets.all(wide ? 32 : 20),
              child: Center(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 1100),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (loadError != null)
                        Padding(
                          padding: const EdgeInsets.only(bottom: 16),
                          child: Text(
                            loadError!,
                            style: const TextStyle(color: Colors.red),
                          ),
                        ),
                      content,
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
      bottomNavigationBar: wide
          ? null
          : NavigationBar(
              selectedIndex: tab,
              onDestinationSelected: (v) => setState(() => tab = v),
              destinations: const [
                NavigationDestination(
                  icon: Icon(Icons.space_dashboard_outlined),
                  label: 'Painel',
                ),
                NavigationDestination(
                  icon: Icon(Icons.checklist_rounded),
                  label: 'Tarefas',
                ),
                NavigationDestination(
                  icon: Icon(Icons.shield_outlined),
                  label: 'Segurança',
                ),
              ],
            ),
    );
  }

  Widget heading(String eyebrow, String title, String description) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text(
        eyebrow,
        style: const TextStyle(
          color: teal,
          fontSize: 12,
          fontWeight: FontWeight.bold,
          letterSpacing: 1.6,
        ),
      ),
      const SizedBox(height: 10),
      Text(title, style: Theme.of(context).textTheme.headlineLarge),
      const SizedBox(height: 10),
      Text(
        description,
        style: const TextStyle(color: Color(0xFF597078), fontSize: 16),
      ),
      const SizedBox(height: 28),
    ],
  );
  Widget panel(Widget child, {Color color = Colors.white}) => Container(
    width: double.infinity,
    padding: const EdgeInsets.all(24),
    decoration: BoxDecoration(
      color: color,
      borderRadius: BorderRadius.circular(24),
      border: Border.all(color: const Color(0xFFE2E7E2)),
    ),
    child: child,
  );
  Widget dashboard() => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      heading(
        'PLANEJAMENTO COM TRANQUILIDADE',
        'Um passo de cada vez.',
        'Organize seus estudos e reserve tempo para o que importa.',
      ),
      panel(
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Seu próximo passo',
              style: TextStyle(color: Colors.white70),
            ),
            const SizedBox(height: 12),
            Text(
              pending.isEmpty
                  ? 'Seu planejamento começa aqui.'
                  : pending.first.title,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 26,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              pending.isEmpty
                  ? 'Adicione uma tarefa e transforme intenção em ação.'
                  : '${pending.first.subject} · ${pending.first.minutes} min · ${dateString(pending.first.deadline)}',
              style: const TextStyle(color: Colors.white70),
            ),
            const SizedBox(height: 20),
            FilledButton.icon(
              onPressed: addTask,
              icon: const Icon(Icons.add),
              label: const Text('Nova tarefa'),
              style: FilledButton.styleFrom(
                backgroundColor: Colors.white,
                foregroundColor: navy,
              ),
            ),
          ],
        ),
        color: navy,
      ),
      const SizedBox(height: 20),
      LayoutBuilder(
        builder: (context, c) {
          final cards = [
            metric('A fazer', '${pending.length}', Icons.schedule),
            metric(
              'Concluídas',
              '${tasks.length - pending.length}',
              Icons.task_alt,
            ),
            metric(
              'Tempo planejado',
              '${pending.fold<int>(0, (sum, t) => sum + t.minutes)} min',
              Icons.timelapse,
            ),
          ];
          return Wrap(
            spacing: 16,
            runSpacing: 16,
            children: cards
                .map(
                  (w) => SizedBox(
                    width: c.maxWidth > 650
                        ? (c.maxWidth - 32) / 3
                        : c.maxWidth,
                    child: w,
                  ),
                )
                .toList(),
          );
        },
      ),
      const SizedBox(height: 28),
      const Text(
        'Em breve',
        style: TextStyle(
          fontWeight: FontWeight.bold,
          fontSize: 22,
          color: navy,
        ),
      ),
      const SizedBox(height: 12),
      if (pending.isEmpty) empty() else ...pending.take(3).map(taskCard),
      const SizedBox(height: 20),
      TextButton.icon(
        onPressed: sample,
        icon: const Icon(Icons.science_outlined),
        label: const Text('Adicionar exemplos fictícios'),
      ),
    ],
  );
  Widget metric(String label, String value, IconData icon) => panel(
    Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, color: teal),
        const SizedBox(height: 16),
        Text(
          value,
          style: const TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.bold,
            color: navy,
          ),
        ),
        Text(label),
      ],
    ),
  );
  Widget empty() => panel(
    const Column(
      children: [
        Icon(Icons.eco_outlined, size: 42, color: teal),
        SizedBox(height: 12),
        Text(
          'Espaço para um novo começo',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        SizedBox(height: 8),
        Text(
          'Suas tarefas aparecerão aqui. Comece com algo pequeno.',
          textAlign: TextAlign.center,
        ),
      ],
    ),
  );
  Widget taskPage() {
    final visible =
        tasks
            .where(
              (t) =>
                  filter == 'Todas' ||
                  (filter == 'Pendentes' && !t.done) ||
                  (filter == 'Concluídas' && t.done),
            )
            .toList()
          ..sort((a, b) => a.deadline.compareTo(b.deadline));
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        heading(
          'UM PLANO POSSÍVEL',
          'Suas tarefas',
          'Defina prazos, acompanhe o progresso e ajuste seu ritmo.',
        ),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: [
            FilledButton.icon(
              onPressed: addTask,
              icon: const Icon(Icons.add),
              label: const Text('Nova tarefa'),
            ),
            ...['Todas', 'Pendentes', 'Concluídas'].map(
              (f) => ChoiceChip(
                label: Text(f),
                selected: filter == f,
                onSelected: (_) => setState(() => filter = f),
              ),
            ),
          ],
        ),
        const SizedBox(height: 24),
        if (visible.isEmpty) empty() else ...visible.map(taskCard),
      ],
    );
  }

  Widget taskCard(StudyTask task) => Padding(
    padding: const EdgeInsets.only(bottom: 12),
    child: panel(
      Row(
        children: [
          Checkbox(
            value: task.done,
            onChanged: (_) => commit(
              tasks.map((t) => t.id == task.id ? t.toggle() : t).toList(),
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  task.title,
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 17,
                    color: navy,
                    decoration: task.done ? TextDecoration.lineThrough : null,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  '${task.subject} · ${dateString(task.deadline)} · ${task.minutes} min',
                  style: const TextStyle(color: Color(0xFF597078)),
                ),
              ],
            ),
          ),
          IconButton(
            tooltip: 'Excluir tarefa',
            onPressed: () => deleteTask(task),
            icon: const Icon(Icons.delete_outline),
          ),
        ],
      ),
    ),
  );
  Future<void> deleteTask(StudyTask task) async {
    final yes = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Excluir tarefa?'),
        content: Text(task.title),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(c, false),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(c, true),
            child: const Text('Excluir'),
          ),
        ],
      ),
    );
    if (yes == true && mounted)
      commit(tasks.where((t) => t.id != task.id).toList());
  }

  void sample() {
    final now = DateTime.now();
    final prefix = now.microsecondsSinceEpoch.toString();
    if (commit([
      ...tasks,
      StudyTask(
        id: '${prefix}a',
        title: 'Exemplo fictício: revisar frações',
        subject: 'Matemática',
        deadline: DateTime(now.year, now.month, now.day + 1),
        minutes: 25,
      ),
      StudyTask(
        id: '${prefix}b',
        title: 'Exemplo fictício: organizar referências',
        subject: 'Projeto de pesquisa',
        deadline: DateTime(now.year, now.month, now.day + 3),
        minutes: 40,
      ),
    ]))
      notice('Exemplos fictícios adicionados. Não são dados de estudantes.');
  }

  Future<void> addTask() async {
    final title = TextEditingController(),
        subject = TextEditingController(),
        minutes = TextEditingController(text: '30');
    final form = GlobalKey<FormState>();
    var deadline = DateTime.now();
    final result = await showDialog<StudyTask>(
      context: context,
      builder: (c) => StatefulBuilder(
        builder: (c, update) => AlertDialog(
          title: const Text('Um novo passo'),
          content: SizedBox(
            width: 420,
            child: Form(
              key: form,
              child: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    TextFormField(
                      controller: title,
                      maxLength: 200,
                      decoration: const InputDecoration(
                        labelText: 'Título da tarefa',
                      ),
                      validator: (v) => v == null || v.trim().isEmpty
                          ? 'Informe um título'
                          : null,
                    ),
                    TextFormField(
                      controller: subject,
                      maxLength: 200,
                      decoration: const InputDecoration(
                        labelText: 'Disciplina ou projeto',
                      ),
                      validator: (v) => v == null || v.trim().isEmpty
                          ? 'Informe uma disciplina'
                          : null,
                    ),
                    TextFormField(
                      controller: minutes,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(
                        labelText: 'Duração em minutos',
                      ),
                      validator: (v) {
                        final n = int.tryParse(v ?? '');
                        return n == null || n < 1 || n > 1440
                            ? 'Use de 1 a 1440 minutos'
                            : null;
                      },
                    ),
                    const SizedBox(height: 16),
                    OutlinedButton.icon(
                      onPressed: () async {
                        final d = await showDatePicker(
                          context: c,
                          initialDate: deadline,
                          firstDate: DateTime(1900),
                          lastDate: DateTime(2200, 12, 31),
                        );
                        if (d != null) update(() => deadline = d);
                      },
                      icon: const Icon(Icons.calendar_today),
                      label: Text('Prazo: ${dateString(deadline)}'),
                    ),
                  ],
                ),
              ),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(c),
              child: const Text('Cancelar'),
            ),
            FilledButton(
              onPressed: () {
                if (form.currentState!.validate())
                  Navigator.pop(
                    c,
                    StudyTask(
                      id: DateTime.now().microsecondsSinceEpoch.toString(),
                      title: title.text.trim(),
                      subject: subject.text.trim(),
                      deadline: deadline,
                      minutes: int.parse(minutes.text),
                    ),
                  );
              },
              child: const Text('Adicionar'),
            ),
          ],
        ),
      ),
    );
    // Dispose after the dialog route has completed its exit animation.
    Future<void>.delayed(const Duration(seconds: 1), () {
      title.dispose();
      subject.dispose();
      minutes.dispose();
    });
    if (result != null && mounted && commit([...tasks, result]))
      notice('Tarefa salva neste navegador.');
  }

  Widget safetyPage() => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      heading(
        'VOCÊ NO CONTROLE',
        'Segurança e backup',
        'Seus dados ficam neste navegador. Tenha sempre uma cópia.',
      ),
      panel(
        const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(Icons.lock_outline, color: teal, size: 32),
            SizedBox(height: 16),
            Text(
              'Local, sem conta e sem servidor',
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: navy,
              ),
            ),
            SizedBox(height: 12),
            Text(
              'Este app não envia tarefas para um servidor e não utiliza IA. O armazenamento local não é criptografado: outras pessoas com acesso ao dispositivo podem acessá-lo. Evite dados pessoais sensíveis.',
            ),
            SizedBox(height: 12),
            Text(
              'Limpar os dados do navegador, usar uma janela privada ou trocar de dispositivo pode apagar ou tornar seus registros inacessíveis. O backup JSON também não é criptografado. Guarde-o em um lugar seguro.',
            ),
          ],
        ),
      ),
      const SizedBox(height: 20),
      panel(
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Uma cópia para continuar',
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: navy,
              ),
            ),
            const SizedBox(height: 12),
            const Text(
              'Exporte suas tarefas ou cole um backup para restaurar. A importação substitui a lista atual após validar todos os registros.',
            ),
            const SizedBox(height: 20),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: [
                FilledButton.icon(
                  onPressed: loadError == null
                      ? () {
                          try {
                            store.downloadBackup(encodeBackup(tasks));
                            notice(
                              'Download solicitado. Verifique a pasta de downloads.',
                            );
                          } catch (_) {
                            notice('Não foi possível exportar o backup.');
                          }
                        }
                      : null,
                  icon: const Icon(Icons.download),
                  label: const Text('Exportar backup'),
                ),
                OutlinedButton.icon(
                  onPressed: importBackup,
                  icon: const Icon(Icons.upload),
                  label: const Text('Importar backup'),
                ),
              ],
            ),
          ],
        ),
      ),
    ],
  );
  Future<void> importBackup() async {
    final input = TextEditingController();
    String? error;
    await showDialog<void>(
      context: context,
      builder: (c) => StatefulBuilder(
        builder: (c, update) => AlertDialog(
          title: const Text('Restaurar backup'),
          content: SizedBox(
            width: 500,
            child: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    'Substitui todas as tarefas atuais. Exporte uma cópia antes de continuar.',
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: input,
                    maxLines: 8,
                    decoration: const InputDecoration(
                      labelText: 'Cole o JSON do backup',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  if (error != null)
                    Padding(
                      padding: const EdgeInsets.only(top: 12),
                      child: Text(
                        error!,
                        style: const TextStyle(color: Colors.red),
                      ),
                    ),
                ],
              ),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(c),
              child: const Text('Cancelar'),
            ),
            FilledButton(
              onPressed: () {
                try {
                  final next = decodeBackup(input.text);
                  store.saveData(encodeBackup(next));
                  setState(() {
                    tasks = next;
                    loadError = null;
                  });
                  Navigator.pop(c);
                  notice('Backup validado e restaurado neste navegador.');
                } catch (e) {
                  update(
                    () => error = e is FormatException ? e.message.toString() : 'Não foi possível salvar. Os dados anteriores foram preservados.',
                  );
                }
              },
              child: const Text('Validar e substituir'),
            ),
          ],
        ),
      ),
    );
    Future<void>.delayed(const Duration(seconds: 1), input.dispose);
  }
}
