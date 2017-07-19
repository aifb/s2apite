/* Generated By:JavaCC: Do not edit this line. KWRLProgramParserConstants.java */
package org.apache.marmotta.kiwi.reasoner.parser;


/**
 * Token literal values and constants.
 * Generated by org.javacc.parser.OtherFilesGen#start()
 */
public interface KWRLProgramParserConstants {

  /** End of File. */
  int EOF = 0;
  /** RegularExpression Id. */
  int STRLIT = 9;
  /** RegularExpression Id. */
  int AND = 11;
  /** RegularExpression Id. */
  int OR = 12;
  /** RegularExpression Id. */
  int NOT = 13;
  /** RegularExpression Id. */
  int THEN = 14;
  /** RegularExpression Id. */
  int TYPE = 15;
  /** RegularExpression Id. */
  int LEFTP = 16;
  /** RegularExpression Id. */
  int RIGHTP = 17;
  /** RegularExpression Id. */
  int INCONSISTENCY = 18;
  /** RegularExpression Id. */
  int URI = 19;
  /** RegularExpression Id. */
  int NS_URI = 20;
  /** RegularExpression Id. */
  int VARIABLE = 21;
  /** RegularExpression Id. */
  int URICONSTRUCTION = 22;
  /** RegularExpression Id. */
  int IDENTIFIER = 23;
  /** RegularExpression Id. */
  int URICHAR = 24;

  /** Lexical state. */
  int DEFAULT = 0;
  /** Lexical state. */
  int IN_COMMENT = 1;
  /** Lexical state. */
  int WithinString = 2;

  /** Literal token values. */
  String[] tokenImage = {
    "<EOF>",
    "\" \"",
    "\"\\r\"",
    "\"\\t\"",
    "\"\\n\"",
    "\"/*\"",
    "<token of kind 6>",
    "\"*/\"",
    "\"\\\"\"",
    "\"\\\"\"",
    "<token of kind 10>",
    "\",\"",
    "\";\"",
    "\"not\"",
    "\"->\"",
    "\"^^\"",
    "\"(\"",
    "\")\"",
    "\"inconsistency\"",
    "<URI>",
    "<NS_URI>",
    "<VARIABLE>",
    "\"uri\"",
    "<IDENTIFIER>",
    "<URICHAR>",
    "\"@prefix\"",
    "\":\"",
    "\"<\"",
    "\">\"",
    "\".\"",
    "\"\\\"\\\"\"",
  };

}