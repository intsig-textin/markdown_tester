### 3.1 Components of Tool Learning

![0_0.png](0_0.png)

![0_4.png](0_4.png)

![0_1.png](0_1.png)

![0_2.png](0_2.png)

![0_3.png](0_3.png)

![0_5.png](0_5.png)

![0_6.png](0_6.png)

![0_7.png](0_7.png)

**Figure 3**: Illustration of the tool learning framework, where we display the human user and four core ingredients of the framework: tool set, controller, perceiver, and environment. The user sends an instruction to the controller, which then makes decisions and executes tools in the environment. The perceiver receives feedback from both the environment and the user and summarizes them to the controller.

Controller. The controller $C$ serves as the “brain” for tool learning framework and is typically modeled using a foundation model. The purpose of the controller $C$ is to provide a feasible and precise plan for using tools to fulfill the user's request. To this end, $C$ should understand user intent as well as the relationship between the intent and available tools, and then develop a plan to select the appropriate tools for tackling tasks, which will be discussed in § 3.2.1. In cases where the query is complex and targets a high-level task, $C$ may need to decompose the task into multiple sub-tasks, which requires foundational models to have powerful planning and reasoning capabilities (§ 3.2.2).

Perceiver. The perceiver $P$ is responsible for processing the user's and the environment's feedback and generating a summary for the controller. Simple forms of feedback processing include concatenating the user and environment feedback or formatting the feedback using a pre-defined template. The summarized feedback is then passed to the controller to assist its decision-making. By observing this feedback, the controller can determine whether the generated plan is effective and whether there are anomalies during the execution that need to be addressed. Under more complex scenarios, the perceiver should be able to support multiple modalities, such as text, vision, and audio, to capture the diverse nature of feedback from the user and the environment.

### 3.1.2 Connecting the Components

Formally, assume we have a tool set $\mathcal{T}$, which the controller can utilize to accomplish certain tasks. At time step $t$, environment $\mathcal{E}$ provides feedback $e_t$ on the tool execution. The perceiver $P$ receives the user feedback $f_t$ and the environment feedback $e_t$, and generates summarized feedback $x_t$. Typically, the perceiver can be achieved by pre-defined rules (e.g., concatenating $f_t$ and $e_t$) to form $x_t$, or modeled with complex neural models. The controller $C$ generates a plan $a_t$, which selects and executes an appropriate tool from $\mathcal{T}$. This process can be formulated as the following probability distribution:

$$
p_C(a_t) = p_{θ_C}(a_t | x_t, H_t, q),
$$

where $θ_C$ denotes the parameters of $C$, $q$ denotes the user query or instruction, and $H_t = \{(x_τ, a_τ)\}_{τ=1}^{t-1}$ denotes the history feedback and plans. In its simplest form, a generated plan $a_t$ can simply be a specific action for tool