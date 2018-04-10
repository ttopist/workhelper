import re
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# --------------------
def to_java_name(name, first_upper=False):
    name_list = name.split('_')
    return_name = [];
    for word in name_list:
        if len(word) > 0 and word[0].isalpha():
            return_name.append(
                (word[0] if len(return_name) == 0 and first_upper == False else word[0].upper()) + word[1:])
        else:
            return_name.append(word)
    return ''.join(return_name)


def to_java_type(type):
    dict = {
        "VARCHAR.*": "String",
        "LONGTEXT": "String",
        "MEDIUMTEXT":"String",
        "CHAR":"String",
        "INTEGER": "Integer",
        "DOUBLE":"Double",
        "BIGINT":"Long",
        "DECIMAL": "BigIntger",
        "DATETIME": "Date",
        "DATE": "Date"
    }
    for key in dict:
        if re.match(key, type) != None:
            return dict[key]
    return 'NoneClass' + to_java_name(type, True)


def hibernatemodel(name, columns_list):
    return_text = []
    return_text.append('Package com.' + to_java_name(name))
    return_text.append('@Entity')
    # print('@Table(name = "csmbp_efficiency_efficiencymail_view_day", catalog = "csmbp_efficiency")')
    return_text.append('@Table(name = "' + name + '")')
    return_text.append('public class ' + to_java_name(name, True) + '{')
    for tuple in columns_list:
        return_text.append('private %s %s;' % (to_java_type(tuple[1]), to_java_name(tuple[0])))
    for tuple in columns_list:
        column_name = tuple[0]
        column_type = tuple[1]
        if tuple[2]:
            return_text.append('@Id')
        return_text.append('''
	@Column(name = "%s")
	public %s get%s() {
		return this.%s;
	}

	public void set%s(%s %s) {
		this.%s = %s;
	}''' % (column_name, to_java_type(column_type), to_java_name(column_name, True), to_java_name(column_name),
            to_java_name(column_name, True), to_java_type(column_type), to_java_name(column_name),
            to_java_name(column_name), to_java_name(column_name)))

        pass
    return_text.append('}')
    return '\n'.join(return_text)


# --------------------

outputdir = ''
dburl = 'mysql+pymysql://root:123456@127.0.0.1:3306/elk?charset=utf8'

engine = create_engine(dburl, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)
tables = Base.metadata.tables

for name in tables:
    table = tables[name];
    #print(table)
    columns = table.get_children();
    #print(columns)
    columns_list = [];
    for c in columns:
        d = c.__dict__
        #print(d)
        name = d['name']
        type = str(d['type'])
        primary_key = d['primary_key']
        nullable = d['nullable']
        #print(name, type, primary_key, nullable)
        columns_list.append((name, type, primary_key, nullable))
    #print(columns_list)
    print(hibernatemodel(name, columns_list))
