package edu.kit.aifb.ldbwebservice;


import org.openrdf.model.ValueFactory;
import org.openrdf.model.impl.ValueFactoryImpl;
import org.semanticweb.yars.nx.Resource;


public class MEXCORE {



	public static final String NAMESPACE = "http://mex.aksw.org/mex-core#";

	/** {@code dbo} **/
	public static final String PREFIX = "mex-core";

	public static final Resource MEMORY;


	static {
		ValueFactory factory = ValueFactoryImpl.getInstance();

		// Properties:
		MEMORY = new Resource(MEXCORE.NAMESPACE + "memory");

	}

}
