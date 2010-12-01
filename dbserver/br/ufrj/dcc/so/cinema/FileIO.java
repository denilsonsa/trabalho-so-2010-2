package br.ufrj.dcc.so.cinema;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import com.google.common.base.Charsets;
import com.google.common.io.Files;

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
		return Files.toString(new File(filename), Charsets.UTF_8);
	}
}
