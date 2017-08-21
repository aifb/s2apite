package edu.kit.aifb.ldbwebservice;

import java.util.ArrayList;
import java.util.Iterator;

import org.openrdf.model.Statement;
import org.openrdf.repository.RepositoryException;

import info.aduna.iteration.CloseableIteration;


@SuppressWarnings("serial")
public class ClosableList<S extends Statement, E extends RepositoryException> extends ArrayList<S> implements CloseableIteration<Statement, RepositoryException> {

	Iterator<S> iter = super.iterator();

	public ClosableList () {
		this.modCount = 0;
	}

	@Override
	public boolean hasNext() {

		return iter.hasNext();
	}

	@Override
	public S next() {
		if ( hasNext() ) {
			this.modCount = 0;
			return iter.next();
		} else {
			return null;
		}
	}

	@Override
	public void close() {
		//super.clear();
	}



	public boolean add(S e) {
		return super.add(e);
	}

	@Override
	public void remove() throws RepositoryException {
		// TODO Auto-generated method stub
		iter.remove();
	}

}
