package edu.kit.aifb.ldbwebservice;

import org.apache.marmotta.commons.vocabulary.LDP;
import org.openrdf.model.URI;
import org.openrdf.model.Value;
import org.openrdf.model.ValueFactory;
import org.openrdf.model.impl.ValueFactoryImpl;
import org.semanticweb.yars.nx.Resource;

public class STEP {
	
	public static final String NAMESPACE = "http://step.aifb.kit.edu/";

    /** {@code step} **/
    public static final String PREFIX = "step";

	public static final URI LinkedDataWebService;
	public static final URI StartAPI;
	public static final URI Output;
	public static final Resource Target;
	public static final Resource BayesNode;
	
	public static final URI hasWebService;
	public static final URI hasProgram;
	public static final URI hasValue;
	public static final URI hasModel;
	public static final URI hasResult;
	public static final Resource hasOutput;

	public static final URI hasStartAPI;
	

	
    static {
        ValueFactory factory = ValueFactoryImpl.getInstance();
        
        // Classes:

        LinkedDataWebService = factory.createURI(STEP.NAMESPACE, "LinkedDataWebService");
        
        StartAPI =  factory.createURI(STEP.NAMESPACE, "StartAPI");
        
        Output = factory.createURI(STEP.NAMESPACE, "Output");
        
        Target = new Resource(STEP.NAMESPACE + "Target");
        
        BayesNode = new Resource(STEP.NAMESPACE + "BayesNode");
        
        
        // Predicates:
        
        hasWebService = factory.createURI(STEP.NAMESPACE, "hasWebService");

        hasProgram = factory.createURI(STEP.NAMESPACE, "hasProgram");
        
        hasValue = factory.createURI(STEP.NAMESPACE, "hasValue");
        
        hasModel = factory.createURI(STEP.NAMESPACE, "hasModel");
        
        hasOutput = new Resource(STEP.NAMESPACE + "hasOutput");
        
        hasResult = factory.createURI(STEP.NAMESPACE, "hasResult");
        
        hasStartAPI = factory.createURI(STEP.NAMESPACE, "hasStartAPI");
    }

}
