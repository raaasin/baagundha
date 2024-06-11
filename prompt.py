#due to some recent errors removed this prompt and sticked with basic version 1 prompt

prompt="""
fit into a normalized 5-star system.

Guidelines

Energy:

0 points for ≤ 335 kJ/100g (solid foods) or ≤ 33 kJ/100mL (liquid foods)
1 point for each 67 kJ/100g increase (solid foods) or each 6.7 kJ/100mL increase (liquid foods)
Up to a maximum of 10 points

Saturated Fat:

0 points for ≤ 1g/100g or ≤ 0.1g/100mL
1 point for each 1.4g/100g increase (solid foods) or each 0.14g/100mL increase (liquid foods)
Up to a maximum of 10 points

Total Sugars:

0 points for ≤ 1g/100g or ≤ 0.5g/100mL
1 point for each 4.5g/100g increase (solid foods) or each 2.25g/100mL increase (liquid foods)
Up to a maximum of 10 points

Sodium:

0 points for ≤ 90mg/100g or ≤ 30mg/100mL
1 point for each 270mg/100g increase (solid foods) or each 90mg/100mL increase (liquid foods)
Up to a maximum of 10 points

Positive Nutrients (Modifying Points):
Protein:

0 points for ≤ 1g/100g or ≤ 0.1g/100mL
1 point for each 1.4g/100g increase (solid foods) or each 0.14g/100mL increase (liquid foods)
Up to a maximum of 5 points

Dietary Fibre:

0 points for ≤ 0.9g/100g or ≤ 0.9g/100mL
1 point for each 1g/100g increase (solid foods) or each 1g/100mL increase (liquid foods)
Up to a maximum of 5 points
Fruit, Vegetables, Nuts, and Legumes (FVNL):

0 points for ≤ 40% FVNL
1 point for each 10% FVNL increase
Up to a maximum of 8 points

Scoring:
Baseline Points (Negative Nutrients): Sum of energy, saturated fat, total sugars, and sodium points.
Modifying Points (Positive Nutrients): Sum of protein, dietary fibre, and FVNL points.
Normalized Health Star Calculation:
Raw Score = Baseline Points - Modifying Points
Normalization:
Assume Min Raw Score = 0
Assume Max Raw Score = 40 (assuming the theoretical maximum for simplification)
Normalize to 5 stars:
Star Rating
=
0.5
+
(
Raw Score
40
×
(
5
−
0.5
)
)
Star Rating=0.5+( 
40
Raw Score
​
 ×(5−0.5))
Example Calculation:
Baseline Points:

Energy = 5, Saturated Fat = 3, Sugars = 4, Sodium = 3 (Total = 15)
Modifying Points:

Protein = 2, Dietary Fibre = 3, FVNL = 4 (Total = 9)
Raw Score: 15 (Baseline Points) - 9 (Modifying Points) = 6

Star Rating:

Star Rating
=
0.5
+
(
6
40
×
(
5
−
0.5
)
)
Star Rating=0.5+( 
40
6
​
 ×(5−0.5))

=
0.5
+
(
0.15
×
4.5
)
=0.5+(0.15×4.5)

=
0.5
+
0.675
=0.5+0.675

=
1.175
=1.175
Thus, the product would get a star rating of approximately 1.2 stars.

Summary Guidelines
Use the above parameters to evaluate products:

Energy: 0 to 10 points (less is better)
Saturated Fat: 0 to 10 points (less is better)
Total Sugars: 0 to 10 points (less is better)
Sodium: 0 to 10 points (less is better)
Protein: 0 to 5 points (more is better)
Dietary Fibre: 0 to 5 points (more is better)
FVNL: 0 to 8 points (more is better)
Normalize the raw score (Baseline Points - Modifying Points) to fit within a 5-star rating system using the provided formula. This ensures the rating system is both consistent and easy to interpret for consumers.
"""