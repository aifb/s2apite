-- Licensed to the Apache Software Foundation (ASF) under one or more
-- contributor license agreements.  See the NOTICE file distributed with
-- this work for additional information regarding copyright ownership.
-- The ASF licenses this file to You under the Apache License, Version 2.0
-- (the "License"); you may not use this file except in compliance with
-- the License.  You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
DROP INDEX idx_justification_triple ON reasoner_justifications;
DROP INDEX idx_just_supp_rules_just ON reasoner_just_supp_rules;
DROP INDEX idx_just_supp_rules_rule ON reasoner_just_supp_rules;
DROP INDEX idx_just_supp_triples_just ON reasoner_just_supp_triples;
DROP INDEX idx_just_supp_triples_triple ON reasoner_just_supp_triples;

DROP TABLE IF EXISTS reasoner_just_supp_rules;
DROP TABLE IF EXISTS reasoner_just_supp_triples;
DROP TABLE IF EXISTS reasoner_justifications;
DROP TABLE IF EXISTS reasoner_program_rules;
DROP TABLE IF EXISTS reasoner_rules;
DROP TABLE IF EXISTS reasoner_program_namespaces;
DROP TABLE IF EXISTS reasoner_programs;
