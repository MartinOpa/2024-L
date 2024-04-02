package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func calc(a int, b int, op rune) (int, string) {
	res := 0

	switch op {
	case '+':
		res = a + b
	case '-':
		res = a - b
	case '*':
		res = a * b
	case '/':
		if b == 0 {
			return 0, "ERROR"
		}
		res = a / b
	}

	return res, ""
}

func eval(expr string) (int, string) {
	a, b, res := 0, 0, 0
	op := ' '
	err := ""
	is_op := false

	for i := 0; i < len(expr); i++ {
		char := rune(expr[i])

		switch char {

		case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
			b = (b * 10) + int(char-'0')
			is_op = false
		case '+', '-', '*', '/':
			if is_op {
				return 0, "ERROR"
			}

			if op != ' ' {
				a, err = calc(a, b, op)
				if err != "" {
					return 0, err
				}

				b = 0
				op = ' '
			} else {
				a = b
				b = 0
			}

			is_op = true
			op = char
		case ' ':
			continue
		case '(':
			bracket_count := 1
			inner_expr, inner_err := "", ""
			i++

			for (i < len(expr)) && bracket_count > 0 {
				if expr[i] == '(' {
					bracket_count++
				}

				if expr[i] == ')' {
					bracket_count--
				}

				if bracket_count > 0 {
					inner_expr += string(expr[i])
					i++
				}
			}

			if bracket_count != 0 {
				return 0, "ERROR"
			}

			b, inner_err = eval(inner_expr)
			if inner_err != "" {
				return 0, "ERROR"
			}

			if op != ' ' {
				is_op = false
				b, err = calc(a, b, op)
				if err != "" {
					return 0, err
				}
				op = ' '
			}

		default:
			return 0, "ERROR"
		}

	}

	if is_op {
		return 0, "ERROR"
	}

	if op != ' ' {
		res, err = calc(a, b, op)
		if err != "" {
			return 0, err
		}
	} else {
		res = a
	}

	return res, ""
}

func main() {
	input := ""
	fmt.Scanln(&input)

	num, err := strconv.Atoi(input)
	if err != nil {
		fmt.Println("Error: ", err)
		return
	}

	scanner := bufio.NewScanner(os.Stdin)
	var results []string
	for i := 0; i < num; i++ {
		if scanner.Scan() {
			expr := scanner.Text()

			res, errStr := eval(expr)
			if errStr == "" {
				expr := strconv.Itoa(res)
				results = append(results, expr)
			} else {
				results = append(results, errStr)
			}
		}
	}

	for _, res := range results {
		fmt.Println(res)
	}
}
