package br.ufrj.dcc.so.cinema;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;

//import com.google.common.base.Charsets;
//import com.google.common.io.Files;

public class FileIO {
	
	public final String PREFIX = "data/";

	// The table name (the filename without prefix/suffix)
	public String name;

	// The actual in-disk filename
	public String filename;

	
	public FileIO(String name) {
		// XXX: Não é feita nenhuma checagem a respeito do nome de arquivo recebido.
		this.name = name;
		this.filename = PREFIX + name + ".data";
	}
	
	public void write(String s) throws IOException {
		FileWriter file_writer = new FileWriter(filename);
		file_writer.write(s);
		file_writer.close();
	}
	
	public String read() throws IOException {
		//return Files.toString(new File(filename), Charsets.UTF_8);
		return read_file_to_string(new File(filename));
	}
	
	
	public String read_file_to_string(File file) throws IOException {
		// This function is based on code from this answer: 
		// http://stackoverflow.com/questions/326390/how-to-create-a-java-string-from-the-contents-of-a-file/2224519#2224519
		// It is based on Google's Guava "Files.toString()" method.

		InputStream in = new FileInputStream(file);
		byte[] b  = new byte[(int) file.length()];
		int len = b.length;
		int total = 0;

		while (total < len) {
		  int result = in.read(b, total, len - total);
		  if (result == -1) {
		    break;
		  }
		  total += result;
		}

		return new String(b);
	}
}
