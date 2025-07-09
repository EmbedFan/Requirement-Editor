# Requirement document for Requirement Editor  
&nbsp;&nbsp;1030 Comm: *This project is for providiing application to writing requirement documents. The requirements has a document level title and sub sections with sub titles. A requirement documentum is a list of classified requirements, that shall be testable and implementable clearly. The document contain comments to give more information to make clear thinks.*  
&nbsp;&nbsp;**Requirement representation in data**  
&nbsp;&nbsp;&nbsp;&nbsp;1000 Req: The requirements shall be saved in data structure, that represents the hierarchy of the requirements.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1001 Req: Every requirement item shall be built from the following items: ID, Type: [TITLE, SUBTITLE, REQUIREMENT, COMMENT], Description, Implemented [TRUE, FALSE], Tested [TRUE, FALSE], Version [M.m], Baselined [integer], Deleted [TRUE, FALSE].  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1002 Req: The ID shall be a unique integer. Once an ID has been assigned and the item is later removed, that ID shall never be reused.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1003 Req: The type shall be one of the following unique enum values: [TITLE, SUBTITLE, REQUIREMENT, COMMENT].  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1004 Req: The description itself shall be a well-worded, easy to understand, not sophisticated high-level sentence or sentences that form a requirement or a comment.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1005 Req: The "Implemented" field shall indicate whether the requirement has been implemented, and shall store a boolean value: [TRUE, FALSE].  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1006 Req: The "Tested" field shall indicate whether the requirement has been tested, and shall store a boolean value: [TRUE, FALSE].  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1009 Comm: *Testing means the requirement has been validated through an appropriate process such as manual verification, automated test execution, or review to ensure it behaves as expected and fulfills its purpose.*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1007 Req: The "Version" field shall store the version number in the format M.m, where M is the major version and m is the minor version. These numbers shall be positive integers.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1008 Comm: *Examples — 1.0, 2.5, 3.12, 10.1 are valid version numbers. Values like 0.-1, 2.a, or 1.1.1 are invalid.*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1012 Req: The "Baselined" field shall be a positive integer between 0 and INTMAX.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1013 Comm: *The baseline means a set of requirements at a specific point in the project's lifetime. When a baseline is created, all requirements with a "false" deleted flag and the highest version number are duplicated with the new baseline number recorded in each copy. It means the document can have more than one baseline, and it is possible to make differences between them or print them out as separate documents.*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1014 Req: The "Deleted" field shall indicate whether a requirement is logically deleted. A deleted item shall remain in the database, shall be ignored during baseline creation and in the active view, but shall be available for review if needed.  
&nbsp;&nbsp;&nbsp;&nbsp;1010 Req: Every document shall be saved into a database (type is not defined at the moment).  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1011 Comm: *The database can be SQLite or any kind of Python structure saved in a file in a form it can be reloaded easily.*

&nbsp;&nbsp;**User Interface Requirements**  
&nbsp;&nbsp;&nbsp;&nbsp;1020 Req: The application shall provide a user interface that allows hierarchical editing of requirement items.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1021 Req: The UI shall allow users to create, edit, delete, and reorder requirements using drag-and-drop functionality.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1022 Req: The UI shall visually distinguish between requirement types using icons or formatting.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1023 Req: The UI shall allow filtering by Implemented, Tested, and Baselined status.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1024 Req: The UI shall support export and import of the document in HTML and Markdown format.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1025 Req: The UI shall support baseline version comparison and difference highlighting.