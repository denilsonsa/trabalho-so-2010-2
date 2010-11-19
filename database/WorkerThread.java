import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;

public class WorkerThread extends Thread {

	private Socket socket;
	private InputStream raw_input;
	private OutputStream raw_output;
	private PrintWriter output;
	private BufferedReader input;
	

	public WorkerThread(Socket incoming) throws IOException {
		socket = incoming;
		raw_input  = socket.getInputStream();
		raw_output = socket.getOutputStream();
		input = new BufferedReader(new InputStreamReader(raw_input));
		output = new PrintWriter(raw_output, true);
		System.out.print("New thread created\n");
	}

	public void run() {
		try {
			System.out.print("Running this new thread...\n");
			output.write("Hello, welcome to this new thread.\r\n");
			while(true) {
				String s;
				s = input.readLine();
				if( s == null )
					break;
				System.out.print("Received: " + s + "\n");
				// Ou usa .print() e depois .flush()
				// Ou usa .println() ou .format() pois eles dão flush automaticamente
				output.print("You said: " + s + "\r\n");
				output.flush();
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.print("Bye bye, thread...\n");
	}

}
