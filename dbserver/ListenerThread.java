import java.net.ServerSocket;
import java.net.Socket;

public class ListenerThread {

	public static void main(String args[]) {
		try {
			ServerSocket server_socket = null;

			int porta = 1234;
			server_socket = new ServerSocket(porta);
			System.out.println("Escutando porta " + Integer.toString(porta));

			while(true) {
				Socket incoming = server_socket.accept();
				Thread new_thread = new WorkerThread(incoming);
				new_thread.start();
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
