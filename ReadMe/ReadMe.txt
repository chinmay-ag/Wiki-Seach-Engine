Steps to run the code:
----------------------------
Dependencies:

--keep the extracted code into same folder as the source code.
--create 3 directories: 
		1) folder: To store the temporary files generated to store the posting lists.(This directory will be deleted later)
		2) output_files: To store the final index segregated into file after applying k way merge sort on temporary files.It also 					 stores a offset file to store output_file offsets for 2 level indexing.It also contains a file to record total 				 number of documents required in tf-idf calculation.
		3) title: To store mapping between docId's and the actual titles. It also stores a toffset file to store title offsets for 2 			          level indexing.
--Requirements: python 3
------------------------------

Running the code:

creating index:
	set the path of the dump in the file wiki_indexer.
	run wiki indexer as:
				python wiki_indexer.py
running query:
	 python query_search.py
