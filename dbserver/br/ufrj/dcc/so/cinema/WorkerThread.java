package br.ufrj.dcc.so.cinema;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.SocketException;

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
			process_input();
			socket.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.print("Bye bye, thread...\n");
	}
	

	// Vai lendo a entrada e repassa para parse_command()
	public void process_input() throws IOException {
		while(true) {
			String s;
			s = input.readLine();
			if( s == null )
				break;
			if( !parse_command(s) )
				break;
		}
	}
	
	// Processa um único comando.
	// Em caso de "sync", chama recusivamente o process_input() dentro de um bloco synchronized().
	// Returns true if should continue parsing, false to stop parsing.
	public Boolean parse_command(String cmdline) throws IOException {
		if( cmdline == null )
			return false;

		String[] tokens = cmdline.split("\\s");
		//for( String i : tokens) {
		//	System.out.println("--"+i+"--");
		//}
		if( tokens.length == 1 )
		{
			String action = tokens[0];

			if( action.equals("TRANSACTION") )
			{
				// TODO: Implement this... Criar um semáforo.
			}
			else if( action.equals("RELEASE") )
			{
				return false;
			}
			else if( action.equals("###") )
			{
				// This should not happen
				return false;
			}
		}
		else if( tokens.length == 2 )
		{
			String action = tokens[0];
			String target = tokens[1];
			if( action.equals("GET") )
			{
				FileIO f = ListenerThread.fileIOFactory.get_FileIO(target);
				output.write(f.read());
				output.write("\n###\n");
				output.flush();
				return true;
			}
			else if( action.equals("PUT") )
			{
				FileIO f = ListenerThread.fileIOFactory.get_FileIO(target);
				String s = read_until_end();
				f.write(s);
				return true;
			}
			else if( action.equals("SYNC") )
			{
				FileIO f = ListenerThread.fileIOFactory.get_FileIO(target);
				synchronized (f) {
					process_input();
				}
				return true;
			}
		}

		// This is an error... Not sure what to do, so let's just go on.
		return true;
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
