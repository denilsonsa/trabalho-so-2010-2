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
	private Boolean has_lock;
	

	public WorkerThread(Socket incoming) throws IOException {
		has_lock = false;

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
			read_and_process_input();
			socket.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.print("Bye bye, thread...\n");
	}
	

	// Vai lendo a entrada e repassa para parse_command()
	public void read_and_process_input() throws IOException, InterruptedException {
		try {
			while(true) {
				String s;
				s = input.readLine();
				if( s == null )
					break;
				parse_command(s);
			}
		} finally {
			if( has_lock )
				ListenerThread.IOLock.release();
		}
	}
	
	// Processa um único comando.
	public void parse_command(String cmdline) throws IOException, InterruptedException {
		if( cmdline == null )
			return;

		String[] tokens = cmdline.split("\\s");
		if( tokens.length == 1 )
		{
			String action = tokens[0];

			if( action.equals("ACQUIRE") )
			{
				if( !has_lock )
				{
					ListenerThread.IOLock.acquire();
					has_lock = true;
				}
			}
			else if( action.equals("RELEASE") )
			{
				if( has_lock )
				{
					ListenerThread.IOLock.release();
					has_lock = false;
				}
			}
			else if( action.equals("###") )
			{
				// This should not happen
				return;
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
			}
			else if( action.equals("PUT") )
			{
				FileIO f = ListenerThread.fileIOFactory.get_FileIO(target);
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
