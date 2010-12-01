OBJECTS = \
	ListenerThread.class \
	WorkerThread.class

CLASSPATH = -cp br/ufrj/dcc/so/cinema:google-gson-1.6/gson-1.6.jar:guava-r07/guava-r07.jar

#Basic rules
.PHONY: all clean run
all: $(OBJECTS)

clean:
	for a in $(OBJECTS) ; do \
		rm -f $$a ; \
	done

#run: $(OBJECTS)
#	java ListenerThread $(CLASSPATH)
run:
	java br.ufrj.dcc.so.cinema.ListenerThread $(CLASSPATH)

#The variables:
# $@ - The name of the target of the rule.
# $? - The names of all the prerequisites that are newer than the target.
# $< - The name of the first prerequisite.
# $^ - The names of all the prerequisites.

#Pattern-rules
%.class: %.java
	javac $< $(CLASSPATH)
