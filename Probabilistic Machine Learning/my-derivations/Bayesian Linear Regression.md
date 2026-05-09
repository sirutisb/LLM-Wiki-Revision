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

Instead of a single weight $w$, we now have a weight vector $\mathbf{w} = (w_1, w_2, \dots, w_D)$ for $D$ input features $\mathbf{x} = (x_1, x_2, \dots, x_D)$:

$$
y_i = \mathbf{w}^T \mathbf{x}_i + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2)
$$

- Each coefficient $w_j$ controls the influence of feature $x_j$ (effect of one feature while holding others fixed).

**Likelihood** (same i.i.d. assumption, just vectorised):

$$
p(\mathbf{y} \mid \mathbf{X}, \mathbf{w}, \sigma^2) = \prod_{i=1}^n \mathcal{N}(y_i \mid \mathbf{w}^T \mathbf{x}_i, \sigma^2)
$$

**MLE solution** — setting $\nabla_{\mathbf{w}} \ell = 0$ gives the normal equations:

$$
\mathbf{w}_{MLE} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}
$$

This directly generalises the simple case: when $D=1$ and $\mathbf{X}$ is just the column vector $\mathbf{x}$, we recover $w_{MLE} = \frac{\sum x_i y_i}{\sum x_i^2}$.
