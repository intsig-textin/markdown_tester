# Components of Tool Learning

Representation of the tool, while a real environment involves actual interaction with the physical tool. Virtual environments have the advantage of being easily accessible and replicable, allowing for more cost-effective training for models. However, virtual environments may not fully replicate the complexities of the real-world environment, leading to overfitting and poor generalization (Hansen et al., 2021). On the other hand, real environments provide a more realistic context but may be more challenging to access and involve greater costs.

# Controller

The controller C serves as the “brain” for tool learning framework and is typically modeled using a foundation model. The purpose of the controller C is to provide a feasible and precise plan for using tools to fulfill the user’s request. To this end, C should understand user intent as well as the relationship between the intent and available tools, and then develop a plan to select the appropriate tools for tackling tasks, which will be discussed in § 3.2.1. In cases where the query is complex and targets a high-level task, C may need to decompose the task into multiple sub-tasks, which requires foundational models to have powerful planning and reasoning capabilities (§ 3.2.2).

# Perceiver

The perceiver P is responsible for processing the user’s and the environment’s feedback and generating a summary for the controller. Simple forms of feedback processing include concatenating the user and environment feedback or formatting the feedback using a pre-defined template. The summarized feedback is then passed to the controller to assist its decision-making. By observing this feedback, the controller can determine whether the generated plan is effective and whether there are anomalies during the execution that need to be addressed. Under more complex scenarios, the perceiver should be able to support multiple modalities, such as text, vision, and audio, to capture the diverse nature of feedback from the user and the environment.

# Connecting the Components

Formally, assume we have a tool set T, which the controller can utilize to accomplish certain tasks. At time step t, environment E provides feedback et on the tool execution. The perceiver P receives the user feedback ft and the environment feedback et, and generates summarized feedback xt. Typically, the perceiver can be achieved by pre-defined rules (e.g., concatenating ft and et) to form xt, or modeled with complex neural models. The controller C generates a plan at, which selects and executes an appropriate tool from T. This process can be formulated as the following probability distribution:

pC (at) = pθC (at | xt, Ht, q), (1)

where θC denotes the parameters of C, q denotes the user query or instruction, and Ht = {(xs, as)}s=0denotest−1 the history feedback and plans. In its simplest form, a generated plan at can simply be a specific action for tool