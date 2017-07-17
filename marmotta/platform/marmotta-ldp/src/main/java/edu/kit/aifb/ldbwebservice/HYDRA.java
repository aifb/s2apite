package edu.kit.aifb.ldbwebservice;


import org.openrdf.model.ValueFactory;
import org.openrdf.model.impl.ValueFactoryImpl;
import org.semanticweb.yars.nx.Resource;


/**
 * @see http://www.hydra-cg.com/spec/latest/core/ 
 * 
 * @author sba
 *
 */
public class HYDRA {
	
	public static final String NAMESPACE = "http://www.w3.org/ns/hydra/core#";

    /** {@code hydra} **/
    public static final String PREFIX = "hydra";

    // classes
	public static final Resource ApiDocumentation;
	public static final Resource Class;
	public static final Resource Collection;
	public static final Resource Error;
	public static final Resource IriTemplate;
	public static final Resource IriTemplateMapping;
	public static final Resource Link;
	public static final Resource Operation;
	public static final Resource PartialCollectionView;
	public static final Resource Resource;
	public static final Resource Status;
	public static final Resource SupportedProperty;
	public static final Resource TemplatedLink;
	public static final Resource VariableRepresentation;
	
	// properties
	public static final Resource apiDocumentation;
	public static final Resource description;
	public static final Resource entrypoint;
	public static final Resource expects;
	public static final Resource first;
	public static final Resource freetextQuery;
	public static final Resource last;
	public static final Resource mapping;
	public static final Resource member;
	public static final Resource method;
	public static final Resource next;
	public static final Resource operation;
	public static final Resource possibleStatus;
	public static final Resource previous;
	public static final Resource property;
	public static final Resource readable;
	public static final Resource required;
	public static final Resource returns;
	public static final Resource search;
	public static final Resource statusCode;
	public static final Resource supportedClass;
	public static final Resource supportedOperation;
	public static final Resource supportedProperty;
	public static final Resource template;
	public static final Resource title;
	public static final Resource totalItems;
	public static final Resource variable;
	public static final Resource variableRepresentation;
	public static final Resource view;
	public static final Resource writeable;

	

	
    static {
        ValueFactory factory = ValueFactoryImpl.getInstance();
        
        // Classes:
    	ApiDocumentation = new Resource(HYDRA.NAMESPACE + "ApiDocumentation");
    	Class = new Resource(HYDRA.NAMESPACE + "Class");
    	Collection = new Resource(HYDRA.NAMESPACE + "Collection");
    	Error = new Resource(HYDRA.NAMESPACE + "Error");
    	IriTemplate = new Resource(HYDRA.NAMESPACE + "IriTemplate");
    	IriTemplateMapping = new Resource(HYDRA.NAMESPACE + "IriTemplateMapping");
    	Link = new Resource(HYDRA.NAMESPACE + "Link");
    	Operation = new Resource(HYDRA.NAMESPACE + "Operation");
    	PartialCollectionView = new Resource(HYDRA.NAMESPACE + "PartialCollectionView");
    	Resource = new Resource(HYDRA.NAMESPACE + "Resource");
    	Status = new Resource(HYDRA.NAMESPACE + "Status");
    	SupportedProperty = new Resource(HYDRA.NAMESPACE + "SupportedProperty");
    	TemplatedLink = new Resource(HYDRA.NAMESPACE + "TemplatedLink");
    	VariableRepresentation = new Resource(HYDRA.NAMESPACE + "VariableRepresentation");
        
        
        // Predicates:
    	apiDocumentation = new Resource(HYDRA.NAMESPACE + "apiDocumentation");
    	description = new Resource(HYDRA.NAMESPACE + "description");
    	entrypoint = new Resource(HYDRA.NAMESPACE + "entrypoint");
    	expects = new Resource(HYDRA.NAMESPACE + "expects");
    	first = new Resource(HYDRA.NAMESPACE + "first");
    	freetextQuery = new Resource(HYDRA.NAMESPACE + "freetextQuery");
    	last = new Resource(HYDRA.NAMESPACE + "last");
    	mapping = new Resource(HYDRA.NAMESPACE + "mapping");
    	member = new Resource(HYDRA.NAMESPACE + "member");
    	method = new Resource(HYDRA.NAMESPACE + "method");
    	next = new Resource(HYDRA.NAMESPACE + "next");
    	operation = new Resource(HYDRA.NAMESPACE + "operation");
    	possibleStatus = new Resource(HYDRA.NAMESPACE + "possibleStatus");
    	previous = new Resource(HYDRA.NAMESPACE + "previous");
    	property = new Resource(HYDRA.NAMESPACE + "property");
    	readable = new Resource(HYDRA.NAMESPACE + "readable");
    	required = new Resource(HYDRA.NAMESPACE + "required");
    	returns = new Resource(HYDRA.NAMESPACE + "returns");
    	search = new Resource(HYDRA.NAMESPACE + "search");
    	statusCode = new Resource(HYDRA.NAMESPACE + "statusCode");
    	supportedClass = new Resource(HYDRA.NAMESPACE + "supportedClass");
    	supportedOperation = new Resource(HYDRA.NAMESPACE + "supportedOperation");
    	supportedProperty = new Resource(HYDRA.NAMESPACE + "supportedProperty");
    	template = new Resource(HYDRA.NAMESPACE + "template");
    	title = new Resource(HYDRA.NAMESPACE + "title");
    	totalItems = new Resource(HYDRA.NAMESPACE + "totalItems");
    	variable = new Resource(HYDRA.NAMESPACE + "variable");
    	variableRepresentation = new Resource(HYDRA.NAMESPACE + "variableRepresentation");
    	view = new Resource(HYDRA.NAMESPACE + "view");
    	writeable = new Resource(HYDRA.NAMESPACE + "writeable");
    }

}
