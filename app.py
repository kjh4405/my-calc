import 'package:flutter/material.dart';

void main() => runApp(const TradingXApp());

class TradingXApp extends StatelessWidget {
  const TradingXApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0A0E21),
        primaryColor: const Color(0xFF00F0FF),
      ),
      home: const LoginScreen(),
    );
  }
}

// --- 로그인 화면 ---
class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        padding: const EdgeInsets.all(30),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.auto_graph, size: 80, color: Color(0xFF00F0FF)),
            const SizedBox(height: 20),
            const Text('TRADING X', style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, letterSpacing: 5)),
            const SizedBox(height: 40),
            TextField(decoration: InputDecoration(hintText: 'ID', filled: true, fillColor: Colors.white10, border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)))),
            const SizedBox(height: 15),
            TextField(obscureText: true, decoration: InputDecoration(hintText: 'Password', filled: true, fillColor: Colors.white10, border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)))),
            const SizedBox(height: 30),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF00F0FF), foregroundColor: Colors.black, padding: const EdgeInsets.all(15)),
                onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const Dashboard())),
                child: const Text('ENTER PLATFORM', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// --- 대시보드 및 리베이트 현황 ---
class Dashboard extends StatelessWidget {
  const Dashboard({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('TRADING X DASHBOARD'), centerTitle: true, elevation: 0, backgroundColor: Colors.transparent),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            _card("My Total Earnings", "\$5,420.00", Colors.cyanAccent),
            const SizedBox(height: 15),
            Row(
              children: [
                Expanded(child: _miniCard("Direct Ref", "24 명", "Level 2")),
                const SizedBox(width: 10),
                Expanded(child: _miniCard("Small Leg", "62 명", "Level 3")),
              ],
            ),
            const SizedBox(height: 20),
            const Text("Subscription Plan", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            _planTile("1 Month", "\$100", "50% Bonus"),
            _planTile("6 Months", "\$500", "50% Bonus"),
            _planTile("15 Months", "\$1,000", "50% Bonus (HOT)"),
          ],
        ),
      ),
    );
  }

  Widget _card(String t, String v, Color c) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(25),
      decoration: BoxDecoration(color: c.withOpacity(0.1), borderRadius: BorderRadius.circular(20), border: Border.all(color: c.withOpacity(0.5))),
      child: Column(children: [Text(t), const SizedBox(height: 10), Text(v, style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: c))]),
    );
  }

  Widget _miniCard(String t, String v, String s) {
    return Container(
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(color: Colors.white10, borderRadius: BorderRadius.circular(15)),
      child: Column(children: [Text(t), Text(v, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)), Text(s, style: const TextStyle(color: Colors.grey, fontSize: 12))]),
    );
  }

  Widget _planTile(String t, String p, String b) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: ListTile(title: Text(t), subtitle: Text(b), trailing: Text(p, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.orangeAccent))),
    );
  }
}
