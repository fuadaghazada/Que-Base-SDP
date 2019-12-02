
import fasttext as ft

model = ft.train_supervised('model.train', epoch = 2000)

print(model.labels)
def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

print_results(*model.test('model.test'))
model.save_model("model_final.bin")
#model_graph = ft.train_supervised('graph_data.txt')
#x = model_array.predict("Alice is a kindergarten teacher. She wants to give some candies to the children in her class.  All the children sit in a line and each of them has a rating score according to his or her performance in the class.  Alice wants to give at least 1 candy to each child. If two children sit next to each other, then the one with the higher rating must get more candies. Alice wants to minimize the total number of candies she must buy. For example, assume her students' ratings are [4, 6, 4, 5, 6, 2].  She gives the students candy in the following minimal amounts: [1, 2, 1, 2, 3, 1].  She must buy a minimum of 10 candies.   Function Description Complete the candies function in the editor below.  It must return the minimum number of candies Alice must buy.   candies has the following parameter(s):   n: an integer, the number of children in the class   arr: an array of integers representing the ratings of each student   Input Format The first line contains an integer, , the size of .  Each of the next  lines contains an integer  indicating the rating of the student at position . Constraints     Output Format Output a single line containing the minimum number of candies Alice must buy. Sample Input 0 Sample Output 0 Explanation 0 Here 1, 2, 2 is the rating. Note that when two children have equal rating, they are allowed to have different number of candies. Hence optimal distribution will be 1, 2, 1. Sample Input 1 Sample Output 1 Explanation 1 Optimal distribution will be  Sample Input 2 Sample Output 2 Explanation 2 Optimal distribution will be .")
#y= model_graph.predict("There are a total of n courses you have to take, labeled from 0 to n-1. Some courses may have prerequisites, for example to take course 0 you have to first take course 1, which is expressed as a pair: [0,1] Given the total number of courses and a list of prerequisite pairs, is it possible for you to finish all courses? Example 1: Input: 2, [[1,0]]  Output: true Explanation: There are a total of 2 courses to take.               To take course 1 you should have finished course 0. So it is possible. Example 2: Input: 2, [[1,0],[0,1]] Output: false Explanation: There are a total of 2 courses to take.               To take course 1 you should have finished course 0, and to take course 0 you should              also have finished course 1. So it is impossible.  Note:  The input prerequisites is a graph represented by a list of edges, not adjacency matrices. Read more about how a graph is represented. You may assume that there are no duplicate edges in the input prerequisites.")
print('')