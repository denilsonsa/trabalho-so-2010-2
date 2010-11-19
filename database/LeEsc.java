import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;

public class LeEsc {
	  public static void main(String args[])  
	    {  
	        try {
	        	String nome_arquivo = "saida.txt";

	        	BufferedWriter output = new BufferedWriter(new FileWriter(nome_arquivo));
				System.out.print("Escrevendo...\n");
	        	output.write("Ola Mundo!\n");
	        	output.close();
	        	
	        	BufferedReader input = new BufferedReader(new FileReader(nome_arquivo));
				System.out.print("Lendo...\n");
				System.out.print(input.readLine());
				input.close();
			} catch (Exception e) {
				e.printStackTrace();
			} 
	        
	    }  
}
