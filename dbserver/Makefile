OBJECTS = \
	br/ufrj/dcc/so/cinema/FileIO.class \
	br/ufrj/dcc/so/cinema/FileIOFactory.class \
	br/ufrj/dcc/so/cinema/WorkerThread.class \
	br/ufrj/dcc/so/cinema/ListenerThread.class

#Basic rules
.PHONY: all clean run
all: $(OBJECTS)

clean:
	for a in $(OBJECTS) ; do \
		rm -fv $$a ; \
	done

run: $(OBJECTS)
	java br.ufrj.dcc.so.cinema.ListenerThread

#The variables:
# $@ - The name of the target of the rule.
# $? - The names of all the prerequisites that are newer than the target.
# $< - The name of the first prerequisite.
# $^ - The names of all the prerequisites.

#Pattern-rules
%.class: %.java
	javac $<
