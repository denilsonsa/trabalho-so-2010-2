package br.ufrj.dcc.so.cinema;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import com.google.common.base.Charsets;
import com.google.common.io.Files;

//import com.google.gson.Gson;
//import com.google.gson.reflect.TypeToken;

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
/*
	public void write(Entidade[] list) throws IOException {
		Gson gson = new Gson();
		FileWriter file_writer = new FileWriter(filename);
		file_writer.write(gson.toJson(list));
		file_writer.close();
	}
	
	public Entidade[] read() throws FileNotFoundException {
		Gson gson = new Gson();
		FileReader file_reader = new FileReader(filename);
		Type return_type = new TypeToken<Entidade[]>() {}.getType();
		return gson.fromJson(file_reader, return_type);
	}
*/
}
