Definitions:
$$
\begin{aligned}
x &= (x_1,\dots,x_n) \\
w &\in \mathbb{R} \\
\sigma^2 &> 0 \\
y_i \mid x_i, w, \sigma^2 &\sim \mathcal{N}(wx_i, \sigma^2) \\
\end{aligned}
$$

We can say that for any value $x_i$ the corresponding $y_i$ is given by:
$$
y_i = wx_i + \epsilon_i
$$
where
$$
\epsilon_i \sim \mathcal{N}(0,\sigma^2)
$$

For simplicity, let $\theta = (w,\sigma^2)$, then

$$
p(y_i\mid x_i,\theta) =
\frac{1}{\sigma\sqrt{2\pi}}
e^{-\frac{1}{2}\left(\frac{y_i-wx_i}{\sigma}\right)^2}
$$

$$
p(y\mid x,\theta) =
\prod_{i=1}^n p(y_i\mid x_i,\theta)
$$

$$
\log p(y\mid x,\theta) =
\sum_{i=1}^n \log\bigl(p(y_i\mid x_i,\theta)\bigr)
$$

$$
\ell(\theta) =
\sum_{i=1}^n
\left(
-\log(\sigma\sqrt{2\pi})
-
\frac{1}{2}
\left(
\frac{y_i-wx_i}{\sigma}
\right)^2
\right)
$$

$$
\frac{\partial \ell(\theta)}{\partial w}
=
\frac{1}{\sigma^2}
\sum_{i=1}^n
x_i\left(y_i-wx_i\right)
$$

$$
\sum_{i=1}^n
x_i\left(y_i-wx_i\right)
=
0
$$

$$
\sum_{i=1}^n x_i y_i
-
w\sum_{i=1}^n x_i^2
=
0
$$

$$
\sum_{i=1}^n x_i y_i
=
w\sum_{i=1}^n x_i^2
$$

$$
w_{MLE} =
\frac{
\sum_{i=1}^n x_i y_i
}{
\sum_{i=1}^n x_i^2
}
$$


---
Multiple Linear Regression:
