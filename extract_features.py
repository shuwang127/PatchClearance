import os
import re
import Levenshtein
import random

# global path.
rootPath = './'
posPath = rootPath + '/security_patch/'
negPath = rootPath + '/random_commit/'

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
# global
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
	Process('F:\\_Workspace\\Patch\\security_patch\\realData\\CWE_16_Configuration\\CVE-2009-1243-30842f2989aacfaba3ccb39829b3417be9313dbe.txt', '1')
	# read the positive files (1).
	for root, ds, fs in os.walk(posPath):
		for file in fs:
			filename = os.path.join(root, file)
			#print(filename)
			#Process(filename, '1')
	# read the negative files (0).
	for root, ds, fs in os.walk(negPath):
		for file in fs:
			filename = os.path.join(root, file)
			#print(filename)
			#Process(filename, '0')
	return

def Process(filename, goldtruth):
	# get the name and label
	name.append(filename)
	label.append(goldtruth)
	# get features.
	GetMutualInfo(filename)
	deletion, addition = GetDiffHunkFunc(filename)
	GetLineInfo(deletion, addition)

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
	print(deletion)
	print(addition)
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



if __name__ == '__main__':
	main()