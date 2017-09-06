package edu.kit.aifb.ldbwebservice;

import org.openrdf.model.ValueFactory;
import org.openrdf.model.impl.ValueFactoryImpl;
import org.semanticweb.yars.nx.Resource;

public class DBO {

	public static final String NAMESPACE = "http://dbpedia.org/ontology/";

	/** {@code dbo} **/
	public static final String PREFIX = "dbo";

	public static final Resource CPU;


	static {
		ValueFactory factory = ValueFactoryImpl.getInstance();

		// Properties:
		CPU = new Resource(DBO.NAMESPACE + "cpu");

	}

}