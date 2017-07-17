package edu.kit.aifb.ldbwebservice;


import org.openrdf.model.ValueFactory;
import org.openrdf.model.impl.ValueFactoryImpl;
import org.semanticweb.yars.nx.Resource;

public class STEP {
	
	public static final String NAMESPACE = "http://step.aifb.kit.edu/";

    /** {@code step} **/
    public static final String PREFIX = "step";

	public static final Resource LinkedDataWebService;
	public static final Resource StartAPI;
	public static final Resource Output;
	public static final Resource Target;
	public static final Resource BayesNode;
	
	public static final Resource hasWebService;
	public static final Resource hasProgram;
	public static final Resource hasValue;
	public static final Resource hasModel;
<<<<<<< HEAD
=======
	public static final Resource hasResult;
>>>>>>> branch 'Marcel_BayesNet' of https://gitlab.com/usu-research-step/s2apite.git
	public static final Resource hasOutput;
<<<<<<< HEAD
	public static final Resource hasBayesNode;
	public static final Resource hasResult;
	public static final Resource hasStartAPI;
	public static final Resource hasProbabilities;
	public static final Resource hasParents;
	public static final Resource hasName;
=======

	public static final Resource hasStartAPI;

	public static final Resource BayesService;
>>>>>>> branch 'Marcel_BayesNet' of https://gitlab.com/usu-research-step/s2apite.git
	

	
    static {
        ValueFactory factory = ValueFactoryImpl.getInstance();
        
        // Classes:

        LinkedDataWebService = new Resource(STEP.NAMESPACE + "LinkedDataWebService");
<<<<<<< HEAD
=======
        BayesService = new Resource(STEP.NAMESPACE + "BayesService");
>>>>>>> branch 'Marcel_BayesNet' of https://gitlab.com/usu-research-step/s2apite.git
        
<<<<<<< HEAD
        StartAPI =  new Resource(STEP.NAMESPACE+ "StartAPI");
=======
        StartAPI =  new Resource(STEP.NAMESPACE + "StartAPI");
>>>>>>> branch 'Marcel_BayesNet' of https://gitlab.com/usu-research-step/s2apite.git
        
<<<<<<< HEAD
        Output = new Resource(STEP.NAMESPACE+ "Output");
=======
        Output = new Resource(STEP.NAMESPACE + "Output");
>>>>>>> branch 'Marcel_BayesNet' of https://gitlab.com/usu-research-step/s2apite.git
        
        Target = new Resource(STEP.NAMESPACE + "Target");
        
        BayesNode = new Resource(STEP.NAMESPACE + "BayesNode");
        
        
        // Predicates:
        
        hasWebService = new Resource(STEP.NAMESPACE + "hasWebService");

        hasProgram = new Resource(STEP.NAMESPACE + "hasProgram");
        
        hasValue = new Resource(STEP.NAMESPACE + "hasValue");
        
        hasModel = new Resource(STEP.NAMESPACE + "hasModel");
        
        hasOutput = new Resource(STEP.NAMESPACE + "hasOutput");
        
<<<<<<< HEAD
        hasBayesNode = new Resource(STEP.NAMESPACE + "hasBayesNode");
=======
        hasResult = new Resource(STEP.NAMESPACE + "hasResult");
>>>>>>> branch 'Marcel_BayesNet' of https://gitlab.com/usu-research-step/s2apite.git
        
<<<<<<< HEAD
        hasResult = new Resource(STEP.NAMESPACE + "hasResult");
        
        hasStartAPI = new Resource(STEP.NAMESPACE + "hasStartAPI");
        
        hasProbabilities = new Resource(STEP.NAMESPACE + "hasProbabilities");
        
        hasParents = new Resource(STEP.NAMESPACE + "hasParents");
        
        hasName = new Resource(STEP.NAMESPACE + "hasName");
=======
        hasStartAPI = new Resource(STEP.NAMESPACE + "hasStartAPI");
>>>>>>> branch 'Marcel_BayesNet' of https://gitlab.com/usu-research-step/s2apite.git
    }

}
