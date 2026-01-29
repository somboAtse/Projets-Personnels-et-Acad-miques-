alter table adapter drop constraint pk_adapter;
alter table adapter 
add constraint pk_adapter primary key 
(codSpe1,codSpe2,codFiliere);