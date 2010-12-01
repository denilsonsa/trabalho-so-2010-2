package br.ufrj.dcc.so.cinema;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.SocketException;

import com.google.gson.Gson;

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
		// PrintWriter com parâmetro "true" faz o flush automaticamente após
		// chamar os métodos .println() ou .format() (mas não faz flush depois
		// do .print())
		output = new PrintWriter(raw_output, true);
		System.out.print("New thread created\n");
	}

	public void run() {
		try {
			System.out.print("Running this new thread...\n");
			output.println("Hello, welcome to this new thread.");
			while(true) {
				String s;
				s = input.readLine();
				if( s == null )
					break;
				parse_command(s);
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.print("Bye bye, thread...\n");
	}
	
	public void parse_command(String cmdline) throws IOException {
		String[] tokens = cmdline.split("\\s");
		//for( String i : tokens) {
		//	System.out.println("--"+i+"--");
		//}
		if( tokens.length == 2 )
		{
			String action = tokens[0];
			String target = tokens[1];
			if( action.equals("GET") )
			{
				FileIO f = new FileIO(target);
				output.write(f.read());
				output.write("\n###\n");
				output.flush();
			}
			else if( action.equals("PUT") )
			{
				FileIO f = new FileIO(target);
				String s = read_until_end();
				f.write(s);
			}
		}
	}
	
	// Reads until receiving a null, or receiving "###"
	public String read_until_end() throws IOException {
		StringBuilder sb = new StringBuilder();
		while(true)
		{
			String s;
			s = input.readLine();
			if( s == null )
				throw new SocketException("End of socket while reading data...");
			if( s.substring(0, 3).equals("###") )
				break;
			sb.append(s);
		}
		return sb.toString();
	}

}
