package org.apache.marmotta.platform.ldp.webservices;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import aifb.edu.manuelBayes.manuelBayes.Node;

public class Network implements Serializable{

	List<Node> Nodes = new ArrayList<Node>();
	
	
	public Node addNode(String name){
		Nodes.add(new Node(name));
		return Nodes.get(Nodes.size()-1);
	}
}
