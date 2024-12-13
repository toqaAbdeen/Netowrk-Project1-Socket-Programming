package moha;


import java.io.*;
import java.net.*;
import java.util.*;

public class TriviaServer {
    private static final int PORT = 5689;
    private static final int MIN_CLIENTS = 2;
    private static final int ROUND_DURATION = 60000; // 60 seconds
    private static final int ANSWER_DURATION = 90000; // 90 seconds

    private DatagramSocket serverSocket;
    private List<InetSocketAddress> clients = new ArrayList<>();
    private List<String> questions = Arrays.asList(
        "Question 1: What is the capital of France?;A) Paris;B) Rome;C) Berlin;D) Madrid;A",
        "Question 2: What is 5 + 5?;A) 7;B) 10;C) 12;D) 15;B",
        "Question 3: Who wrote 'Hamlet'?;A) Dickens;B) Shakespeare;C) Twain;D) Austen;B"
    );
    private Map<InetSocketAddress, Integer> scores = new HashMap<>();

    public TriviaServer() throws IOException {
        serverSocket = new DatagramSocket(PORT);
    }

    public void start() throws IOException {
        System.out.println("Server started on port " + PORT);

        while (true) {
            // Step 1: Wait for clients to connect
            if (clients.size() < MIN_CLIENTS) {
                System.out.println("Waiting for clients...");
                receiveClientConnection();
                continue;
            }

            System.out.println("Enough clients connected. Starting round...");
            broadcastMessage("ROUND_START");

            // Step 2: Broadcast questions
            for (String question : questions) {
                broadcastMessage(question);
                try {
                    Thread.sleep(ROUND_DURATION);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                // Step 3: Collect answers
                Map<InetSocketAddress, String> answers = collectAnswers();
                processAnswers(question, answers);
            }

            // Step 4: Display scores
            broadcastScores();
            pauseBetweenRounds();
        }
    }

    private void receiveClientConnection() throws IOException {
        byte[] buffer = new byte[1024];
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
        serverSocket.receive(packet);

        InetSocketAddress clientAddress = new InetSocketAddress(packet.getAddress(), packet.getPort());
        if (!clients.contains(clientAddress)) {
            clients.add(clientAddress);
            scores.put(clientAddress, 0);
            System.out.println("New client connected: " + clientAddress);
            sendMessage("WELCOME", clientAddress);
        }
    }

    private void broadcastMessage(String message) throws IOException {
        byte[] buffer = message.getBytes();
        for (InetSocketAddress client : clients) {
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length, client.getAddress(), client.getPort());
            serverSocket.send(packet);
        }
    }

    private Map<InetSocketAddress, String> collectAnswers() throws IOException {
        Map<InetSocketAddress, String> answers = new HashMap<>();
        long startTime = System.currentTimeMillis();

        while (System.currentTimeMillis() - startTime < ANSWER_DURATION) {
            byte[] buffer = new byte[1024];
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            serverSocket.receive(packet);

            InetSocketAddress clientAddress = new InetSocketAddress(packet.getAddress(), packet.getPort());
            String answer = new String(packet.getData(), 0, packet.getLength());
            if (!answers.containsKey(clientAddress)) {
                answers.put(clientAddress, answer);
                System.out.println("Received answer from " + clientAddress + ": " + answer);
            }
        }

        return answers;
    }

    private void processAnswers(String question, Map<InetSocketAddress, String> answers) throws IOException {
        String correctAnswer = question.split(";")[4];
        for (Map.Entry<InetSocketAddress, String> entry : answers.entrySet()) {
            InetSocketAddress client = entry.getKey();
            String answer = entry.getValue();
            if (answer.equals(correctAnswer)) {
                scores.put(client, scores.get(client) + 1);
                sendMessage("CORRECT", client);
            } else {
                sendMessage("WRONG", client);
            }
        }
    }

    private void broadcastScores() throws IOException {
        StringBuilder leaderboard = new StringBuilder("LEADERBOARD:\n");
        for (Map.Entry<InetSocketAddress, Integer> entry : scores.entrySet()) {
            leaderboard.append(entry.getKey()).append(": ").append(entry.getValue()).append(" points\n");
        }
        broadcastMessage(leaderboard.toString());
    }

    private void pauseBetweenRounds() {
        try {
            System.out.println("Pausing between rounds...");
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private void sendMessage(String message, InetSocketAddress client) throws IOException {
        byte[] buffer = message.getBytes();
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length, client.getAddress(), client.getPort());
        serverSocket.send(packet);
    }

    public static void main(String[] args) {
        try {
            TriviaServer server = new TriviaServer();
            server.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}