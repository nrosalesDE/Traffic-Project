FROM public.ecr.aws/lambda/python:3.13

# Copy requirements first so Docker can cache dependency installs
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies into the Lambda task root
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy your function code and project files
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY Transform.py ${LAMBDA_TASK_ROOT}
COPY S3_Functions_transform.py ${LAMBDA_TASK_ROOT}
COPY Transform_Functions.py ${LAMBDA_TASK_ROOT}


# Set the Lambda handler
CMD ["lambda_function.lambda_handler"]