OBJECTS = \
	ListenerThread.class \
	WorkerThread.class

#Basic rules
.PHONY: all clean run
all: $(OBJECTS)

clean:
	for a in $(OBJECTS) ; do \
		rm -f $$a ; \
	done

run: $(OBJECTS)
	java ListenerThread

#The variables:
# $@ - The name of the target of the rule.
# $? - The names of all the prerequisites that are newer than the target.
# $< - The name of the first prerequisite.
# $^ - The names of all the prerequisites.

#Pattern-rules
%.class: %.java
	javac $<
