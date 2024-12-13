package moha;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class TriviaCilent {



    private static final String SERVER_IP = "127.0.0.1";
    private static final int SERVER_PORT = 5689;

    private DatagramSocket clientSocket;
    private InetAddress serverAddress;

    public TriviaCilent() throws IOException {
        clientSocket = new DatagramSocket();
        serverAddress = InetAddress.getByName(SERVER_IP);
    }

    public void start() throws IOException {
        try (Scanner scanner = new Scanner(System.in)) {
			System.out.println("Connected to server on " + SERVER_IP + ":" + SERVER_PORT);
			sendMessage("JOIN");

			while (true) {
			    String message = receiveMessage();
			    if (message.equals("ROUND_START")) {
			        System.out.println("New round starting...");
			    } else if (message.startsWith("Question")) {
			        System.out.println(message);
			        System.out.print("Your answer: ");
			        String answer = scanner.nextLine();
			        sendMessage(answer);
			    } else if (message.startsWith("LEADERBOARD")) {
			        System.out.println(message);
			    } else {
			        System.out.println(message);
			    }
			}
		} 
    }

    private void sendMessage(String message) throws IOException {
        byte[] buffer = message.getBytes();
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length, serverAddress, SERVER_PORT);
        clientSocket.send(packet);
    }

    private String receiveMessage() throws IOException {
        byte[] buffer = new byte[1024];
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
        clientSocket.receive(packet);
        return new String(packet.getData(), 0, packet.getLength());
    }

    public static void main(String[] args) {
        try {
            TriviaCilent client = new TriviaCilent();
            client.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}