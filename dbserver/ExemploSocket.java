import java.net.ServerSocket;
import java.net.Socket;

public class ExemploSocket {

  public static void main(String args[]) {
		try {
			ServerSocket server_socket = null;
			
			// Porta 1234
			server_socket = new ServerSocket(1234);
			System.out.print("Escutando porta 1234\n");
			
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
