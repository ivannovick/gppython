CREATE TABLE abalone (sex text, length float, diameter float, height float, whole_weight float,
shucked_weight float, viscera_weight float, shell_weight float, rings integer) distributed randomly ;

\copy abalone (sex, length, diameter, height, whole_weight, shucked_weight, viscera_weight, shell_weight, rings)
    FROM 'Downloads/abalone.data' DELIMITER ','
