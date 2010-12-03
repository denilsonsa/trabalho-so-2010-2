package br.ufrj.dcc.so.cinema;

import java.util.HashMap;
import java.util.Map;

public class FileIOFactory {

	private Map<String,FileIO> map;

	public FileIOFactory() {
		map = new HashMap<String,FileIO>();
	}

	public synchronized FileIO get_FileIO(String name) {
		if(!map.containsKey(name)) {
			map.put(name, new FileIO(name));
		}
		return map.get(name);
	}
}
