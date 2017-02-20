package edu.kit.aifb.ldbwebservice;

import org.apache.marmotta.commons.vocabulary.LDP;
import org.openrdf.model.URI;
import org.openrdf.model.ValueFactory;
import org.openrdf.model.impl.ValueFactoryImpl;

public class Vocabulary {
	
	public static final String NAMESPACE = "http://step.aifb.kit.edu/";

    /** {@code step} **/
    public static final String PREFIX = "step";

	public static final URI LinkedDataWebService;
	
	public static final URI StartAPI;
	
    static {
        ValueFactory factory = ValueFactoryImpl.getInstance();

        LinkedDataWebService = factory.createURI(Vocabulary.NAMESPACE, "LinkedDataWebService");
        
        StartAPI =  factory.createURI(Vocabulary.NAMESPACE, "StartAPI");
    }

}
