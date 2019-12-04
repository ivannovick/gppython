CREATE TAbLE test_results (testtype int, testresults int[], test_attr int[]);
INSERT into test_results VALUES
(93723, '{32,131,13,331,323}', '{33,33,33,11,11}'),
(93723, '{21,11,13,34,2}', '{11,11,11,11,11}'),
(93723, '{222,112,212,233,191}', '{33,33,33,33,11}'),
(93723, '{44,12,66,81,99,100}', '{33,44,44,11,44}'),
(93723, '{89,85,80,88,89}', '{11,33,33,11,33}');

CREATE OR REPLACE FUNCTION test_success_check(array_test_results int[])
   RETURNS BOOLEAN
AS $$
    import numpy as np
    narray = np.array(array_test_results)
    return (narray < 100).all()
    $$ LANGUAGE plpythonu;

SELECT testtype, testresults, test_success_check(testresults) FROM test_results;
