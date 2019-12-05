CREATE OR REPLACE FUNCTION chunkit(adata int[])
   returns setof int as $$
        return adata;
    $$ LANGUAGE plpythonu;

CREATE TAbLE test_results (testtype int, testresults int[], test_attr int[]);
INSERT into test_results VALUES
(93723, '{32,131,13,331,323}', '{33,33,33,11,11}'),
(93723, '{21,11,13,34,2}', '{11,11,11,11,11}'),
(93723, '{222,112,212,233,191}', '{33,33,33,33,11}'),
(93723, '{44,12,66,81,99,100}', '{33,44,44,11,44}'),
(93723, '{89,85,80,88,89}', '{11,33,33,11,33}');

SELECT chunkit(testresults)
FROM test_results order by 1
LIMIT 10;
