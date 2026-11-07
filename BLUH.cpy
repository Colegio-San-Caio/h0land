      * BLUH.cpy - BLUH console record (copybook)
       01  BLUH-REC.
           05  BLUH-GRID-X      PIC 9(3) VALUE 16.
           05  BLUH-GRID-Y      PIC 9(3) VALUE 16.
           05  BLUH-BLOCK-X     PIC 9(3) VALUE 16.
           05  BLUH-BLOCK-Y     PIC 9(3) VALUE 16.
           05  BLUH-QUERY       PIC X(80).
           05  BLUH-ANSWER      PIC X(400).
           05  BLUH-MODE        PIC X(4).
               88  BLUH-STUB    VALUE 'STUB'.
               88  BLUH-LLM     VALUE 'LLM '.
