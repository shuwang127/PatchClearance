import os
import re
import Levenshtein
import pandas as pd

# global path.
rootPath = '../'
posPath = rootPath + '/security_patch/'
negPath = rootPath + '/random_commit/'
csvPath = rootPath + '/csvfiles/'

# keyword definition.
MI_keyword = ["overflow", "leak", "buffer", "race", "integer", "null", "dereference", "free", "lock", "byte", \
			  "directory", "bound", "loop", "uninitialized", "stack", "memory","padding", "infinite", "double", \
			  "array", "capture", "pointer", "permission", "size", "length", "division", "crash", "key", "root", "leak"]
# arithmetic operations.
ari_op2 = ["++", "--"]
ari_op1 = ["=", "+", "-", "*", "/", "%"]
# relational operations.
rel_op2 = ["==", "!=", ">=", "<="]
rel_op1 = [">", "<"]
# logical operations.
log_op2 = ["&&", "||"]
log_op1 = ["!", "not", "and", "or"]
# bit operations.
bit_op2 = ["<<", ">>", "bitand", "bitor", "xor"]
bit_op1 = ["~", "&", "|", "^"]
# memory keywords.
mem_keyword = ["malloc", "calloc", "realloc", "free", "memset", "memcmp", "memcpy", "memmove", "sizeof", "new", "delete"]
# if keywords.
if_keyword = ["if", "else", "switch", "case", "&&", "||"]
# loop keywords.
loop_keyword = ["for", "while"]
# jump keywords.
jump_keyword = ["break", "continue", "return", "goto", "throw", "assert"]
# C keywords.
c_keywords = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern', \
			  'float', 'for', 'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict', 'return', 'short', 'signed', \
			  'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while', 'bool', \
			  'alignas', 'alignof', 'bool', 'complex', 'imaginary', 'noreturn', 'static_assert', 'thread_local']
# C++ keywords.
cpp_keywords = ['alignas', 'alignof', 'and', 'and_eq', 'asm', 'atomic_cancel', 'atomic_commit', 'atomic_noexcept', 'auto', \
				'bitand', 'bitor', 'bool', 'break', 'case', 'catch', 'char', 'char8_t', 'char16_t', 'char32_t', 'class', \
				'compl', 'concept', 'const', 'consteval', 'constexpr', 'const_cast', 'continue', 'co_await', 'co_return', \
				'co_yield', 'decltype', 'default', 'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum', 'explicit', \
				'export', 'extern', 'false', 'float', 'for', 'friend', 'goto', 'if', 'import', 'inline', 'int', 'long', \
				'module', 'mutable', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq', \
				'private', 'protected', 'public', 'reflexpr', 'register', 'reinterpret_cast', 'requires', 'return', 'short', \
				'signed', 'sizeof', 'static', 'static_assert', 'static_cast', 'struct', 'switch', 'synchronized', 'template', \
				'this', 'thread_local', 'throw', 'true', 'try', 'typedef', 'typeid', 'typename', 'union', 'unsigned', 'using', \
				'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq', 'printf']
# dictionary keywords.
dir_keyword = ["\'\'", "\'.\'", "\'..\'", "\'/../\'", "\'../\'", "\'/..\'", "\'/\'", "\'\\\'", "\'/\\\'",\
				'\"\"', '\".\"', '\"..\"', '\"/../\"', '\"../\"', '\"/..\"', '\"/\"', '\"\\\"', "\'/\\\'"]
# race keywords.
race_keyword = ["release", "lock", "mutex", "unlock"]
# not keywords.
not_keyword = ["==0", "!=0", "==null", "!=null", "!"]

# define cache.
name = []
label = []
MI = []
# diff, hunk, func number.
diff_num = []
hunk_num = []
func_num = []
# line number.
line_num_total = []
line_num_net = []
line_num_del = []
line_num_add = []
# character number.
char_num_total = []
char_num_net = []
char_num_del = []
char_num_add = []
# memory number.
mem_num_total = []
mem_num_net = []
mem_num_del = []
mem_num_add = []
# if number.
if_num_total = []
if_num_net = []
if_num_del = []
if_num_add = []
# jump number.
jump_num_total = []
jump_num_net = []
jump_num_del = []
jump_num_add = []
# loop number.
loop_num_total = []
loop_num_net = []
loop_num_del = []
loop_num_add = []
# arithmetic number.
ari_num_total = []
ari_num_net = []
ari_num_del = []
ari_num_add = []
# relational number.
rel_num_total = []
rel_num_net = []
rel_num_del = []
rel_num_add = []
# logical number.
log_num_total = []
log_num_net = []
log_num_del = []
log_num_add = []
# bit number.
bit_num_total = []
bit_num_net = []
bit_num_del = []
bit_num_add = []
# call number.
call_num_total = []
call_num_net = []
call_num_del = []
call_num_add = []
# variable number.
var_num_total = []
var_num_net = []
var_num_del = []
var_num_add = []
# global similarity.
global_sim = []
global_norm_sim = []
# dictionary number.
dir_num_total = []
dir_num_net = []
dir_num_del = []
dir_num_add = []
# others.
cap_num = []
race_num = []
not_zero = []
preprocess = []

def main():
	'''
	# read the positive files (1).
	for root, ds, fs in os.walk(posPath):
		for file in fs:
			filename = os.path.join(root, file)
			print(filename)
			Process(filename, '1')
	# read the negative files (0).
	for root, ds, fs in os.walk(negPath + 'commit01'):
		for file in fs:
			filename = os.path.join(root, file)
			print(filename)
			Process(filename, '0')
	Write2File(csvPath + 'feature01.csv')
	'''
	folder = 2  # 2-30
	for root, ds, fs in os.walk(negPath + 'commit' + str(folder).zfill(2)):
		for file in fs:
			filename = os.path.join(root, file)
			print(filename)
			Process(filename, '0')
	Write2File(csvPath + 'feature' + str(folder).zfill(2) + '.csv')

	return

def Process(filename, goldtruth):
	# get the name and label
	name.append(filename)
	label.append(goldtruth)
	# get features.
	GetMutualInfo(filename)
	deletion, addition = GetDiffHunkFunc(filename)
	GetLineInfo(deletion, addition)
	GetCharInfo(deletion, addition)
	GetMemInfo(deletion, addition)
	GetIfInfo(deletion, addition)
	GetJumpInfo(deletion, addition)
	GetLoopInfo(deletion, addition)
	GetAriRelLogBit(deletion, addition)
	del_var_list, add_var_list = GetCallVar(deletion, addition)
	GetGlobalSim(deletion, addition)
	GetDirInfo(deletion, addition)
	GetCapInfo(del_var_list, add_var_list)
	GetRaceInfo(deletion, addition)
	GetNotZero(deletion, addition)
	GetPreprocess(deletion, addition)
	return

def GetMutualInfo(filename):
	# read file.
	fp = open(filename, encoding='utf-8', errors='ignore')
	contents = fp.read()
	# get contents after Subject or before diff.
	i = contents.find("Subject:")
	if i > 0:
		j = contents.find("---\n")
		content = contents[i + 8:j - 1].lower()
	else:
		j = contents.find("\ndiff")
		content = contents[:j].lower()
	# get mutual information list.
	MI_list = ""
	for item in MI_keyword:
		MI_list += str(content.count(item)) + ','
	MI.append(MI_list)
	# close file.
	fp.close()
	return

def GetDiffHunkFunc(filename):
	# output initialize.
	deletion = []
	addition = []
	# temp variable.
	diff_n = 0
	hunk_n = 0
	func_list = []
	del_hunk = ""
	add_hunk = ""
	in_diff = 0
	# read file with lines.
	fp = open(filename, encoding='utf-8', errors='ignore')
	while 1:
		line = fp.readline()
		if not line:
			break
		# if line begins with diff, set in_diff = 1.
		if line[:5] == "diff ":
			if (line[line.rfind('.') + 1:-1].lower() in ["c", "c++", "cpp", "h", "h++", "hpp", "cc", "hh", "cxx", "hxx"]) and ("test" not in line.lower()):
				diff_n += 1
				in_diff = 1
			else:
				in_diff = 0
		# if line in the diff part.
		if in_diff == 1:
			# if line begins with @@, get the function name.
			if line[:2] == "@@":
				if (len(line[line.rfind("@@") + 2:-1]) != 0) \
						and (line[line.rfind("@@") + 2:-1] not in func_list) and line[-2:-1] == ')':
					func_list.append(line[line.rfind("@@") + 2:-1])
			# if line begins with +, -, but not ++, --.
			if (line[:1] in ['+', '-']) and (line[:2] not in ["++", "--"]) and (line[:3] not in ["+++", "---"]):
				# if line begins with '/*', '*', '*/'.
				if "/*" or "*" or "*/" in line:
					if ("*/" in line) and ("/*" not in line):
						line = ''
					elif (line[1:].lstrip()[:2] == "/*") or (line[1:].lstrip()[:1] == "*"):
						line = ''
					else:
						i = line.find("/*")
						if i > 0:
							line = line[:i] + "\n"
				# if line begins with '-'.
				if (line[:1] == '-') and (len(line[1:].strip()) != 0):
					del_hunk += line
				# if line begins with '+'
				if (line[:1] == '+') and (len(line[1:].strip()) != 0):
					add_hunk += line
			else:
				# if find a hunk.
				if len(del_hunk) + len(add_hunk) > 0:
					deletion.append(del_hunk)
					addition.append(add_hunk)
					hunk_n += 1
				del_hunk = ""
				add_hunk = ""
	# close the file.
	fp.close()
	# get diff, hunk, func number.
	diff_num.append(diff_n)
	hunk_num.append(hunk_n)
	func_num.append(len(func_list))
	return deletion, addition

def GetLineInfo(deletion, addition):
	# line
	del_line = 0
	add_line = 0
	# find all hunks.
	for i in range(len(deletion)):
		if (len(deletion[i]) != 0):
			del_line += deletion[i].count("\n-") + 1
		if (len(addition[i]) != 0):
			add_line += addition[i].count("\n+") + 1
	# statistic.
	line_num_total.append(add_line + del_line)
	line_num_net.append(add_line - del_line)
	line_num_del.append(del_line)
	line_num_add.append(add_line)
	return del_line, add_line

def GetCharInfo(deletion, addition):
	# char
	del_char = 0
	add_char = 0
	# find all hunks.
	for i in range(len(deletion)):
		if (len(deletion[i]) != 0):
			del_char += len(deletion[i]) - deletion[i].count('\n') - deletion[i].count('\r') - deletion[i].count('\t') - deletion[i].count(' ') - (deletion[i].count("\n-")+1)
		if (len(addition[i]) != 0):
			add_char += len(addition[i]) - addition[i].count('\n') - addition[i].count('\r') - addition[i].count('\t') - addition[i].count(' ') - (addition[i].count("\n+")+1)
	# statistic.
	char_num_total.append(add_char + del_char)
	char_num_net.append(add_char - del_char)
	char_num_del.append(del_char)
	char_num_add.append(add_char)
	return del_char, add_char

def GetMemInfo(deletion, addition):
	# memory information.
	del_mem = 0
	add_mem = 0
	# find all hunks.
	for i in range(len(deletion)):
		for item in mem_keyword:
			if item in deletion[i]:
				del_mem += deletion[i].count(item)
			if item in addition[i]:
				add_mem += addition[i].count(item)
	# statistic.
	mem_num_total.append(add_mem + del_mem)
	mem_num_net.append(add_mem - del_mem)
	mem_num_del.append(del_mem)
	mem_num_add.append(add_mem)
	return del_mem, add_mem

def GetIfInfo(deletion, addition):
	# if keyword
	del_if = 0
	add_if = 0
	# find all hunks.
	for i in range(len(deletion)):
		for item in if_keyword:
			if item in deletion[i]:
				del_if += deletion[i].count(item)
			if item in addition[i]:
				add_if += addition[i].count(item)
	# statistic.
	if_num_total.append(add_if + del_if)
	if_num_net.append(add_if - del_if)
	if_num_del.append(del_if)
	if_num_add.append(add_if)
	return del_if, add_if

def GetJumpInfo(deletion, addition):
	# jump keyword
	del_jump = 0
	add_jump = 0
	# find all hunks.
	for i in range(len(deletion)):
		for term in jump_keyword:
			if term in deletion[i]:
				del_jump += deletion[i].count(term)
			if term in addition[i]:
				add_jump += addition[i].count(term)
	# statistic.
	jump_num_total.append(add_jump + del_jump)
	jump_num_net.append(add_jump - del_jump)
	jump_num_del.append(del_jump)
	jump_num_add.append(add_jump)
	return del_jump, add_jump

def GetLoopInfo(deletion, addition):
	# loop keyword.
	del_loop = 0
	add_loop = 0
	# find all hunks.
	for i in range(len(deletion)):
		for item in loop_keyword:
			if item in deletion[i]:
				del_loop += deletion[i].count(item)
			if item in addition[i]:
				add_loop += addition[i].count(item)
	# statistic.
	loop_num_total.append(add_loop + del_loop)
	loop_num_net.append(add_loop - del_loop)
	loop_num_del.append(del_loop)
	loop_num_add.append(add_loop)
	return del_loop, add_loop

def GetAriRelLogBit(deletion, addition):
	# arithmetic.
	del_ari = 0
	add_ari = 0
	# relational.
	del_rel = 0
	add_rel = 0
	# logical.
	del_log = 0
	add_log = 0
	# bit.
	del_bit = 0
	add_bit = 0
	# find all hunks.
	for i in range(len(deletion)):
		tmp_del = deletion[i][1:].replace("\n-", '')
		tmp_add = addition[i][1:].replace("\n+", '')
		for item in ari_op2:
			del_ari += tmp_del.count(item)
			add_ari += tmp_add.count(item)
			tmp_del = tmp_del.replace(item, '')
			tmp_add = tmp_add.replace(item, '')
		for item in rel_op2:
			del_rel += tmp_del.count(item)
			add_rel += tmp_add.count(item)
			tmp_del = tmp_del.replace(item, '')
			tmp_add = tmp_add.replace(item, '')
		for item in log_op2:
			del_log += tmp_del.count(item)
			add_log += tmp_add.count(item)
			tmp_del = tmp_del.replace(item, '')
			tmp_add = tmp_add.replace(item, '')
		for item in bit_op2:
			del_bit += tmp_del.count(item)
			add_bit += tmp_add.count(item)
			tmp_del = tmp_del.replace(item, '')
			tmp_add = tmp_add.replace(item, '')
		for item in ari_op1:
			del_ari += tmp_del.count(item)
			add_ari += tmp_add.count(item)
			tmp_del = tmp_del.replace(item, '')
			tmp_add = tmp_add.replace(item, '')
		for item in rel_op1:
			del_rel += tmp_del.count(item)
			add_rel += tmp_add.count(item)
			tmp_del = tmp_del.replace(item, '')
			tmp_add = tmp_add.replace(item, '')
		for item in log_op1:
			del_log += tmp_del.count(item)
			add_log += tmp_add.count(item)
			tmp_del = tmp_del.replace(item, '')
			tmp_add = tmp_add.replace(item, '')
		for item in bit_op1:
			del_bit += tmp_del.count(item)
			add_bit += tmp_add.count(item)
			tmp_del = tmp_del.replace(item, '')
			tmp_add = tmp_add.replace(item, '')
	# arithmetic.
	ari_num_total.append(add_ari + del_ari)
	ari_num_net.append(add_ari - del_ari)
	ari_num_del.append(del_ari)
	ari_num_add.append(add_ari)
	# relational.
	rel_num_total.append(add_rel + del_rel)
	rel_num_net.append(add_rel - del_rel)
	rel_num_del.append(del_rel)
	rel_num_add.append(add_rel)
	# logical.
	log_num_total.append(add_log + del_log)
	log_num_net.append(add_log - del_log)
	log_num_del.append(del_log)
	log_num_add.append(add_log)
	# bit.
	bit_num_total.append(add_bit + del_bit)
	bit_num_net.append(add_bit - del_bit)
	bit_num_del.append(del_bit)
	bit_num_add.append(add_bit)
	return del_ari, add_ari, del_rel, add_rel, del_log, add_log, del_bit, add_bit

def GetCallVar(deletion, addition):
	# call and var
	del_func_list = []
	del_var_list = []
	add_func_list = []
	add_var_list = []
	# find all hunks.
	for i in range(len(deletion)):
		tmp_del = deletion[i]
		tmp_add = addition[i]
		# process tmp_del.
		pre_del = ""
		while 1:
			if "\n-" in tmp_del:
				i = tmp_del.find("\n-")
				line = tmp_del[1:i].lstrip()
				tmp_del = tmp_del[i + 1:]
			else:
				line = tmp_del[1:].lstrip()
				tmp_del = ''
			if line[:1] == '#':
				pass
			else:
				while (len(line) > 0):
					mark = re.match('[0-9a-zA-Z\_]+', line)
					if (mark):
						j = mark.end()
						del_var_list.append(line[:j])
						pre_del = line[:j]
						line = line[j:].lstrip()
					else:
						j = re.match('[^\w\s]+', line)
						if (j):
							j = j.end()
							if line[:j][:1] == '(' and re.match('[0-9a-zA-Z\_]+', pre_del):
								del_var_list.remove(pre_del)
								del_func_list.append(pre_del)
							pre_del = line[:j]
							line = line[j:].lstrip()
						else:
							break
			if len(tmp_del) == 0:
				break
		del_var_list = list(set(del_var_list))
		del_func_list = list(set(del_func_list))
		# process tmp_add.
		pre_add = ""
		while 1:
			if "\n+" in tmp_add:
				i = tmp_add.find("\n+")
				line = tmp_add[1:i].lstrip()
				tmp_add = tmp_add[i + 1:]
			else:
				line = tmp_add[1:].lstrip()
				tmp_add = ''
			if line[:1] == '#':
				pass
			else:
				while (len(line) > 0):
					mark = re.match('[0-9a-zA-Z\_]+', line)
					if (mark):
						j = mark.end()
						add_var_list.append(line[:j])
						pre_add = line[:j]
						line = line[j:].lstrip()
					else:
						j = re.match('[^\w\s]+', line)
						if (j):
							j = j.end()
							if line[:j][:1] == '(' and re.match('[0-9a-zA-Z\_]+', pre_add):
								add_var_list.remove(pre_add)
								add_func_list.append(pre_add)
							pre_add = line[:j]
							line = line[j:].lstrip()
						else:
							break
			if len(tmp_add) == 0:
				break
		add_var_list = list(set(add_var_list))
		add_func_list = list(set(add_func_list))
	# call statistic.
	call_num_total.append(len(list(set(del_func_list).union(set(add_func_list)).difference(set(c_keywords + cpp_keywords)))))
	call_num_net.append(len(list(set(add_func_list).difference(set(del_func_list + c_keywords + cpp_keywords)))))
	call_num_del.append(len(list(set(del_func_list).difference(set(c_keywords + cpp_keywords)))))
	call_num_add.append(len(list(set(add_func_list).difference(set(c_keywords + cpp_keywords)))))
	# var statistic.
	var_num_total.append(len(list(set(del_var_list).union(set(add_var_list)).difference(set(c_keywords + cpp_keywords)))))
	var_num_net.append(len(list(set(add_var_list).difference(set(del_var_list + c_keywords + cpp_keywords)))))
	var_num_del.append(len(list(set(del_var_list).difference(set(c_keywords + cpp_keywords)))))
	var_num_add.append(len(list(set(add_var_list).difference(set(c_keywords + cpp_keywords)))))
	return del_var_list, add_var_list

def GetGlobalSim(deletion, addition):
	# global similarity
	tmp_del = ""
	tmp_add = ""
	# find all hunks.
	for i in range(len(deletion)):
		tmp_del += deletion[i]
		tmp_add += addition[i]
	# statistic.
	tmp_del = tmp_del[1:].replace("\n-", '').replace("\n", '').replace("\r", '').replace("\t", '').replace(" ", '')
	tmp_add = tmp_add[1:].replace("\n+", '').replace("\n", '').replace("\r", '').replace("\t", '').replace(" ", '')
	global_sim.append(Levenshtein.distance(tmp_del, tmp_add))  # /(len(tmp_del)*1.0))
	# normalized statistic.
	tmp_del = re.sub(r"[A-Za-z0-9_\.]", 'x', tmp_del)
	tmp_add = re.sub(r"[A-Za-z0-9_\.]", 'x', tmp_add)
	tmp_del = re.sub(r"x*", 'x', tmp_del)
	tmp_add = re.sub(r"x*", 'x', tmp_add)
	global_norm_sim.append(Levenshtein.distance(tmp_del, tmp_add))  # /(len(tmp_del)*1.0))
	return tmp_del, tmp_add

def GetDirInfo(deletion, addition):
	# dir num
	del_dir = 0
	add_dir = 0
	# find all hunks.
	for i in range(len(deletion)):
		for item in dir_keyword:
			if item in deletion[i]:
				del_dir += deletion[i].count(item)
			if item in addition[i]:
				add_dir += addition[i].count(item)
	# statistic.
	dir_num_total.append(add_dir + del_dir)
	dir_num_net.append(add_dir - del_dir)
	dir_num_del.append(del_dir)
	dir_num_add.append(add_dir)
	return del_dir, add_dir

def GetCapInfo(del_var_list, add_var_list):
	# cap_num
	del_cap = []
	add_cap = []
	# match CapList.
	for item in del_var_list:
		if re.match('[A-Z\_]+', item):
			del_cap.append(item)
	for item in add_var_list:
		if re.match('[A-Z\_]+', item):
			add_cap.append(item)
	cap_num.append(len(list(set(add_cap).difference(set(del_cap + add_cap)))))
	return del_cap, add_cap

def GetRaceInfo(deletion, addition):
	# race num
	del_race = 0
	add_race = 0
	# find all hunks.
	for i in range(len(deletion)):
		for item in race_keyword:
			del_race += deletion[i].lower().count(item)
			add_race += addition[i].lower().count(item)
	race_num.append(add_race - del_race)
	return del_race, add_race

def GetNotZero(deletion, addition):
	# not zero
	del_not = 0
	add_not = 0
	# find all hunks.
	for i in range(len(deletion)):
		for item in not_keyword:
			del_not += deletion[i].lower().count(item)
			add_not += addition[i].lower().count(item)
	not_zero.append(add_not - del_not)
	return del_not, add_not

def GetPreprocess(deletion, addition):
	# preprocess statement
	del_pro = 0
	add_pro = 0
	# find all hunks.
	for i in range(len(deletion)):
		del_pro += deletion[i].replace("\n-", '').replace("\n", '').replace("\r", '').replace("\t", '').replace(" ", '').count("-#")
		add_pro += addition[i].replace("\n+", '').replace("\n", '').replace("\r", '').replace("\t", '').replace(" ", '').count("+#")
	preprocess.append(add_pro - del_pro)
	return del_pro, add_pro

def Write2File(filename):
	# write to file
	dset = pd.DataFrame()

	dset['name'] = name
	dset['diff_num'] = diff_num
	dset['hunk_num'] = hunk_num
	dset['func_num'] = func_num

	dset['line_num_total'] = line_num_total
	dset['line_num_net'] = line_num_net
	dset['line_num_del'] = line_num_del
	dset['line_num_add'] = line_num_add

	dset['char_num_total'] = char_num_total
	dset['char_num_net'] = char_num_net
	dset['char_num_del'] = char_num_del
	dset['char_num_add'] = char_num_add

	dset['mem_num_total'] = mem_num_total
	dset['mem_num_net'] = mem_num_net
	dset['mem_num_del'] = mem_num_del
	dset['mem_num_add'] = mem_num_add

	dset['if_num_total'] = if_num_total
	dset['if_num_net'] = if_num_net
	dset['if_num_del'] = if_num_del
	dset['if_num_add'] = if_num_add

	dset['jump_num_total'] = jump_num_total
	dset['jump_num_net'] = jump_num_net
	dset['jump_num_del'] = jump_num_del
	dset['jump_num_add'] = jump_num_add

	dset['loop_num_total'] = loop_num_total
	dset['loop_num_net'] = loop_num_net
	dset['loop_num_del'] = loop_num_del
	dset['loop_num_add'] = loop_num_add

	dset['ari_num_total'] = ari_num_total
	dset['ari_num_net'] = ari_num_net
	dset['ari_num_del'] = ari_num_del
	dset['ari_num_add'] = ari_num_add

	dset['rel_num_total'] = rel_num_total
	dset['rel_num_net'] = rel_num_net
	dset['rel_num_del'] = rel_num_del
	dset['rel_num_add'] = rel_num_add

	dset['log_num_total'] = log_num_total
	dset['log_num_net'] = log_num_net
	dset['log_num_del'] = log_num_del
	dset['log_num_add'] = log_num_add

	dset['bit_num_total'] = bit_num_total
	dset['bit_num_net'] = bit_num_net
	dset['bit_num_del'] = bit_num_del
	dset['bit_num_add'] = bit_num_add

	dset['call_num_total'] = call_num_total
	dset['call_num_net'] = call_num_net
	dset['call_num_del'] = call_num_del
	dset['call_num_add'] = call_num_add

	dset['var_num_total'] = var_num_total
	dset['var_num_net'] = var_num_net
	dset['var_num_del'] = var_num_del
	dset['var_num_add'] = var_num_add

	dset['global_sim'] = global_sim
	dset['global_norm_sim'] = global_norm_sim

	dset['dir_num_total'] = dir_num_total
	dset['dir_num_net'] = dir_num_net
	dset['dir_num_del'] = dir_num_del
	dset['dir_num_add'] = dir_num_add

	dset['cap_num'] = cap_num
	dset['race_num'] = race_num
	dset['not_zero'] = not_zero
	dset['preprocess'] = preprocess

	dset.to_csv(filename)
	return

if __name__ == '__main__':
	main()