import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.Semaphore;

public class WorkerThread extends Thread {

	private Socket socket;
	private InputStream raw_input;
	private OutputStream raw_output;
	private PrintWriter output;
	private BufferedReader input;
	
	class FileProxy {
		public FileProxy(String filename) {
			// TODO
		}
	}
	
	public WorkerThread(Socket incoming) throws IOException {
		socket = incoming;
		raw_input  = socket.getInputStream();
		raw_output = socket.getOutputStream();
		input = new BufferedReader(new InputStreamReader(raw_input));
		output = new PrintWriter(raw_output, true);
		System.out.print("New thread created\n");
		
		//NAO VAI PRECISAR DISSO DE FATO
		Map<String, FileProxy> mapa = new HashMap<String, FileProxy>();
		mapa = Collections.synchronizedMap(mapa);
		
		//O QUE FAZER QUANDO CHEGA UMA REQUISICAO:
		//(ISSO JA NA THREAD)
		String filename = "xxx";
		synchronized(mapa) {
			FileProxy proxy;
			
			if(mapa.containsKey(filename)) {
				proxy = mapa.get(filename);
			} else {
				proxy = new FileProxy(filename);
				mapa.put(filename, proxy);
			}
		}
		
		Semaphore sem = new Semaphore(10);
		
		try {
			synchronized(this) {
				wait(100);
			}
		} catch(Exception e) {
			//
		}
	
		
		//proxy.doCleverAssignmentStuffGayThome(command);
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
